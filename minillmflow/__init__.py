import asyncio
import warnings
            
class BaseNode:
    #  preprocess(): this is for compute intensive preparation tasks, before the LLM call
    #  process(): this is for the LLM call, and should be idempotent for retries
    #  postprocess(): this is to summarize the result and retrun the condition for the successor node
    def __init__(self):
        self.params, self.successors = {}, {}

    def set_params(self, params): # make sure params is immutable
        self.params = params # must be immutable during pre/post/process

    def add_successor(self, node, condition="default"):
        if condition in self.successors:
            warnings.warn(f"Overwriting existing successor for condition '{condition}'")
        self.successors[condition] = node  # maps condition -> successor node
        return node

    def preprocess(self, shared_storage):
        return None # will be passed to process() and postprocess()

    def process(self, shared_storage, prep_result):
        return None # will be passed to postprocess()

    def _process(self, shared_storage, prep_result):
        # Could have retry logic or other wrap logic
        return self.process(shared_storage, prep_result)
        
    def postprocess(self, shared_storage, prep_result, proc_result):
        return "default" # condition for next node
    
    def _run(self, shared_storage):
        prep_result = self.preprocess(shared_storage)
        proc_result = self._process(shared_storage, prep_result)
        return self.postprocess(shared_storage, prep_result, proc_result)
    
    def run(self, shared_storage):
        if self.successors:
            warnings.warn("This node has successor nodes. To run its successors, wrap this node in a parent Flow and use that Flow.run() instead.")
        return self._run(shared_storage)

    def __rshift__(self, other):
        # chaining: node1 >> node2
        return self.add_successor(other)

    def __sub__(self, condition):
        # condition-based chaining: node - "some_condition" >> next_node
        if isinstance(condition, str):
            return _ConditionalTransition(self, condition)
        raise TypeError("Condition must be a string")

class _ConditionalTransition:
    def __init__(self, source_node, condition):
        self.source_node = source_node
        self.condition = condition

    def __rshift__(self, target_node):
        return self.source_node.add_successor(target_node, self.condition)

class Node(BaseNode):
    def __init__(self, max_retries=1):
        super().__init__()
        self.max_retries = max_retries

    def process_after_fail(self, shared_storage, data, exc):
        raise exc

    def _process(self, shared_storage, data):
        for attempt in range(self.max_retries):
            try:
                return super()._process(shared_storage, data)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return self.process_after_fail(shared_storage, data, e)

class BatchNode(Node):
    def preprocess(self, shared_storage):
        # return an iterable of items, one for each run
        return []
    
    def process(self, shared_storage, item): # process() is called for each item
        return None

    def _process(self, shared_storage, items):
        results = []
        for item in items:
            # Here, 'item' is passed in place of 'prep_result' from the BaseNode's perspective.
            r = super()._process(shared_storage, item)
            results.append(r)
        return results

class AsyncNode(Node):
    def postprocess(self, shared_storage, prep_result, proc_result):
        raise NotImplementedError("AsyncNode requires postprocess_async, and should be run in an AsyncFlow")
    
    async def postprocess_async(self, shared_storage, prep_result, proc_result):
        await asyncio.sleep(0)  # trivial async pause (no-op)
        return "default"
    
    async def run_async(self, shared_storage):
        if self.successors:
            warnings.warn("This node has successor nodes. To run its successors, wrap this node in a parent AsyncFlow and use that AsyncFlow.run_async() instead.")
        return await self._run_async(shared_storage)
        
    async def _run_async(self, shared_storage):
        prep_result = self.preprocess(shared_storage)
        proc_result = self._process(shared_storage, prep_result)
        return await self.postprocess_async(shared_storage, prep_result, proc_result)
    
    def _run(self, shared_storage):
        raise RuntimeError("AsyncNode requires asynchronous execution. Use 'await node.run_async()' if inside an async function, or 'asyncio.run(node.run_async())' if in synchronous code.")

class BaseFlow(BaseNode):
    def __init__(self, start_node):
        super().__init__()
        self.start_node = start_node

    def get_next_node(self, current_node, condition):
        next_node = current_node.successors.get(condition, None)
        
        if next_node is None and current_node.successors:
            warnings.warn(f"Flow will end. Condition '{condition}' not found among possible conditions: {list(current_node.successors.keys())}")
        
        return next_node
    
class Flow(BaseFlow):
    def _process(self, shared_storage, params=None):
        current_node = self.start_node
        params = params if params is not None else self.params.copy()
        
        while current_node:
            current_node.set_params(params)
            condition = current_node._run(shared_storage)
            current_node = self.get_next_node(current_node, condition)
            
    def process(self, shared_storage, prep_result):
        raise NotImplementedError("Flow should not process directly")
        
class AsyncFlow(BaseFlow, AsyncNode):
    async def _process_async(self, shared_storage, params=None):
        current_node = self.start_node
        params = params if params is not None else self.params.copy()
        
        while current_node:
            current_node.set_params(params)

            if hasattr(current_node, "run_async") and callable(current_node.run_async):
                condition = await current_node._run_async(shared_storage)
            else:
                condition = current_node._run(shared_storage)

            current_node = self.get_next_node(current_node, condition)

    async def _run_async(self, shared_storage):
        prep_result = self.preprocess(shared_storage)
        await self._process_async(shared_storage)
        return await self.postprocess_async(shared_storage, prep_result, None)

class BaseBatchFlow(BaseFlow):
    def preprocess(self, shared_storage):
        return [] # return an iterable of parameter dictionaries

class BatchFlow(BaseBatchFlow, Flow):
    def _run(self, shared_storage):
        prep_result = self.preprocess(shared_storage)
        
        for param_dict in prep_result:
            merged_params = self.params.copy()
            merged_params.update(param_dict)
            self._process(shared_storage, params=merged_params)
        
        return self.postprocess(shared_storage, prep_result, None)

class BatchAsyncFlow(BaseBatchFlow, AsyncFlow):
    async def _run_async(self, shared_storage):
        prep_result = self.preprocess(shared_storage)
        
        for param_dict in prep_result:
            merged_params = self.params.copy()
            merged_params.update(param_dict)
            await self._process_async(shared_storage, params=merged_params)
            
        return await self.postprocess_async(shared_storage, prep_result, None)