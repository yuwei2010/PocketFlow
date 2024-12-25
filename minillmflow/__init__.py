import asyncio
import warnings
            
class BaseNode:
    #  preprocess(): this is for compute intensive preparation tasks, before the LLM call
    #  process(): this is for the LLM call, and should be idempotent for retries
    #  postprocess(): this is to summarize the result and retrun the condition for the successor node
    def __init__(self):
        self.parameters, self.successors = {}, {}

    def set_parameters(self, params): # make sure params is immutable
        self.parameters = params # must be immutable during pre/post/process

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
    
    def _run(self, shared_storage=None):
        prep = self.preprocess(shared_storage)
        proc = self._process(shared_storage, prep)
        return self.postprocess(shared_storage, prep, proc)
    
    def run(self, shared_storage=None):
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
    """
    A Node whose postprocess step is async.
    You can also override process() to be async if needed.
    """
    def postprocess(self, shared_storage, prep_result, proc_result):
        # Not used in async workflow; define postprocess_async() instead.
        raise NotImplementedError("AsyncNode requires postprocess_async, and should be run in an AsyncFlow")
    
    async def postprocess_async(self, shared_storage, prep_result, proc_result):
        """
        Async version of postprocess. By default, returns "default".
        Override as needed.
        """
        await asyncio.sleep(0)  # trivial async pause (no-op)
        return "default"
    
    async def run_async(self, shared_storage=None):
        if self.successors:
            warnings.warn("This node has successor nodes. To run its successors, wrap this node in a parent AsyncFlow and use that AsyncFlow.run_async() instead.")
        return await self._run_async(shared_storage)
        
    async def _run_async(self, shared_storage=None):
        prep = self.preprocess(shared_storage)
        proc = self._process(shared_storage, prep)
        return await self.postprocess_async(shared_storage, prep, proc)
    
    def _run(self, shared_storage=None):
        raise RuntimeError("AsyncNode requires run_async, and should be run in an AsyncFlow")

class BaseFlow(BaseNode):
    def __init__(self, start_node=None):
        super().__init__()
        self.start_node = start_node

    def get_next_node(self, current_node, condition):
        next_node = current_node.successors.get(condition, None)
        
        if next_node is None and current_node.successors:
            warnings.warn(f"Flow will end. Condition '{condition}' not found among possible conditions: {list(current_node.successors.keys())}")
        
        return next_node
    
class Flow(BaseFlow):
    def _process_flow(self, shared_storage):
        current_node = self.start_node
        while current_node:
            # Pass down the Flow's parameters to the current node
            current_node.set_parameters(self.parameters)
            # Synchronous run
            condition = current_node._run(shared_storage)
            # Decide next node
            current_node = self.get_next_node(current_node, condition)

    def _run(self, shared_storage=None):
        prep_result = self.preprocess(shared_storage)
        self._process_flow(shared_storage)
        return self.postprocess(shared_storage, prep_result, None)

class AsyncFlow(BaseFlow):
    async def _process_flow_async(self, shared_storage):
        current_node = self.start_node
        while current_node:
            current_node.set_parameters(self.parameters)

            # If node is async-capable, call run_async; otherwise run sync
            if hasattr(current_node, "run_async") and callable(current_node.run_async):
                condition = await current_node._run_async(shared_storage)
            else:
                condition = current_node._run(shared_storage)

            current_node = self.get_next_node(current_node, condition)

    async def _run_async(self, shared_storage=None):
        prep_result = self.preprocess(shared_storage)
        await self._process_flow_async(shared_storage)
        return self.postprocess(shared_storage, prep_result, None)

    def _run(self, shared_storage=None):
        try:
            return asyncio.run(self._run_async(shared_storage))
        except RuntimeError as e:
            raise RuntimeError("If you are running in Jupyter, please use `await run_async()` instead of `run()`.") from e
    
class BaseBatchFlow(BaseFlow):
    def preprocess(self, shared_storage):
        return []

class BatchFlow(BaseBatchFlow, Flow):
    def _run(self, shared_storage=None):
        prep_result = self.preprocess(shared_storage)
        all_results = []

        # For each set of parameters (or items) we got from preprocess
        for param_dict in prep_result:
            # Merge param_dict into the Flow's parameters
            original_params = self.parameters.copy()
            self.parameters.update(param_dict)

            # Run from the start node to end
            self._process_flow(shared_storage)

            # Optionally collect results from shared_storage or a custom method
            all_results.append(f"Finished run with parameters: {param_dict}")

            # Reset the parameters if needed
            self.parameters = original_params

class BatchAsyncFlow(BaseBatchFlow, AsyncFlow):
    async def _run_async(self, shared_storage=None):
        prep_result = self.preprocess(shared_storage)
        all_results = []

        for param_dict in prep_result:
            original_params = self.parameters.copy()
            self.parameters.update(param_dict)

            await self._process_flow_async(shared_storage)

            all_results.append(f"Finished async run with parameters: {param_dict}")

            # Reset back to original parameters if needed
            self.parameters = original_params