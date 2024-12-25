import asyncio

class BaseNode:
    """
    A base node that provides:
      - preprocess()
      - process()
      - postprocess()
      - run() -- just runs itself (no chaining)
    """
    def __init__(self):
        self.parameters = {}
        self.successors = {}

    def set_parameters(self, params):
        self.parameters.update(params)

    def add_successor(self, node, condition="default"):
        if condition in self.successors:
            print(f"Warning: overwriting existing successor for condition '{condition}'")
        self.successors[condition] = node
        return node

    def preprocess(self, shared_storage):
        return None

    def process(self, shared_storage, prep_result):
        return None

    def _process(self, shared_storage, prep_result):
        # Could have retry logic or other wrap logic
        return self.process(shared_storage, prep_result)
        
    def postprocess(self, shared_storage, prep_result, proc_result):
        return "default"

    def run(self, shared_storage=None):
        prep = self.preprocess(shared_storage)
        proc = self._process(shared_storage, prep)
        return self.postprocess(shared_storage, prep, proc)

    def __rshift__(self, other):
        """
        For chaining with >> operator, e.g. node1 >> node2
        """
        return self.add_successor(other)

    def __gt__(self, other):
        """
        For chaining with > operator, e.g. node1 > "some_condition"
        then >> node2
        """
        if isinstance(other, str):
            return _ConditionalTransition(self, other)
        elif isinstance(other, BaseNode):
            return self.add_successor(other)
        raise TypeError("Unsupported operand type")

    def __call__(self, condition):
        """
        For node("condition") >> next_node syntax
        """
        return _ConditionalTransition(self, condition)


class _ConditionalTransition:
    """
    Helper for Node > 'condition' >> AnotherNode style
    """
    def __init__(self, source_node, condition):
        self.source_node = source_node
        self.condition = condition

    def __rshift__(self, target_node):
        return self.source_node.add_successor(target_node, self.condition)

# robust running process
class Node(BaseNode):
    def __init__(self, max_retries=1):
        super().__init__()
        self.max_retries = max_retries

    def process_after_fail(self, shared_storage, data, exc):
        raise exc
        # return "fail"

    def _process(self, shared_storage, data):
        for attempt in range(self.max_retries):
            try:
                return super()._process(shared_storage, data)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return self.process_after_fail(shared_storage, data, e)
                
class Flow(BaseNode):
    def __init__(self, start_node=None):
        self.start_node = start_node
        
    def _process(self, shared_storage, _):
        current_node = self.start_node
        while current_node:
            condition = current_node.run(shared_storage)
            current_node = current_node.successors.get(condition, None)
            
    def postprocess(self, shared_storage, prep_result, proc_result):
        return None



class AsyncNode(Node):
    """
    A Node whose postprocess step is async.
    You can also override process() to be async if needed.
    """

    async def postprocess_async(self, shared_storage, prep_result, proc_result):
        """
        Async version of postprocess. By default, returns "default".
        Override as needed.
        """
        await asyncio.sleep(0)  # trivial async pause (no-op)
        return "default"

    async def run_async(self, shared_storage=None):
        """
        Async version of run. 
        If your process method is also async, you'll need to adapt accordingly.
        """
        # We can keep preprocess synchronous or make it async as well,
        # depending on your usage. Here it's left as sync for simplicity.
        prep = self.preprocess(shared_storage)
        
        # process can remain sync if you prefer, or you can define an async process.
        proc = self._process(shared_storage, prep)

        # postprocess is async
        return await self.postprocess_async(shared_storage, prep, proc)


class AsyncFlow(Flow):
    """
    A Flow that can handle a mixture of sync and async nodes.
    If the node is an AsyncNode, calls `run_async`.
    Otherwise, calls `run`.
    """
    async def _process(self, shared_storage, _):
        current_node = self.start_node
        while current_node:
            if hasattr(current_node, "run_async") and callable(current_node.run_async):
                # If it's an async node, await its run_async
                condition = await current_node.run_async(shared_storage)
            else:
                # Otherwise, assume it's a sync node
                condition = current_node.run(shared_storage)

            current_node = current_node.successors.get(condition, None)

    async def run_async(self, shared_storage=None):
        """
        Kicks off the async flow. Similar to Flow.run, 
        but uses our async _process method.
        """
        prep = self.preprocess(shared_storage)
        # Note: flows typically don't need a meaningful process step
        # because the "process" is the iteration through the nodes.
        await self._process(shared_storage, prep)
        return self.postprocess(shared_storage, prep, None)
    
class BatchNode(BaseNode):
    def __init__(self, max_retries=5, delay_s=0.1):
        super().__init__()
        self.max_retries = max_retries
        self.delay_s = delay_s

    def preprocess(self, shared_storage):
        return []

    def process_one(self, shared_storage, item):
        return None

    def process_one_after_fail(self, shared_storage, item, exc):
        print(f"[FAIL_ITEM] item={item}, error={exc}")
        # By default, just return a "fail" marker. Could be anything you want.
        return "fail"

    async def _process_one(self, shared_storage, item):
        for attempt in range(self.max_retries):
            try:
                return await self.process_one(shared_storage, item)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    # If out of retries, let a subclass handle what to do next
                    return await self.process_one_after_fail(shared_storage, item, e)
                await asyncio.sleep(self.delay_s)

    async def _process(self, shared_storage, items):
        results = []
        for item in items:
            r = await self._process_one(shared_storage, item)
            results.append(r)
        return results

class BatchFlow(BaseNode):
    def __init__(self, start_node=None):
        super().__init__()
        self.start_node = start_node

    def preprocess(self, shared_storage):
        return []

    async def _process_one(self, shared_storage, param_dict):
        node_parameters = self.parameters.copy()
        node_parameters.update(param_dict)

        if self.start_node:
            current_node = self.start_node
            while current_node:
                # set the combined parameters
                current_node.set_parameters(node_parameters)
                current_node = await current_node._run_one(shared_storage or {})

    async def _process(self, shared_storage, items):
        results = []
        for param_dict in items:
            await self._process_one(shared_storage, param_dict)
            results.append(f"Ran sub-flow for param_dict={param_dict}")
        return results