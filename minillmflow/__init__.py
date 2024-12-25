import asyncio
import warnings
            
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

    def __sub__(self, condition):
        """
        For chaining with - operator, e.g. node - "some_condition" >> next_node
        """
        if isinstance(condition, str):
            return _ConditionalTransition(self, condition)
        raise TypeError("Condition must be a string")
        

class _ConditionalTransition:
    """
    Helper for Node > 'condition' >> AnotherNode style
    (and also Node - 'condition' >> AnotherNode now).
    """
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
        prep = self.preprocess(shared_storage)
        proc = self._process(shared_storage, prep)
        return await self.postprocess_async(shared_storage, prep, proc)


class BaseFlow(BaseNode):
    """
    Abstract base flow that provides the main logic of:
      - Starting from self.start_node
      - Looping until no more successors
    Subclasses must define how they *call* each node (sync or async).
    """
    def __init__(self, start_node=None):
        super().__init__()
        self.start_node = start_node

    def get_next_node(self, current_node, condition):
        next_node = current_node.successors.get(condition, None)
        
        if next_node is None and current_node.successors:
            warnings.warn(f"Flow will end. Condition '{condition}' not found among possible conditions: {list(current_node.successors.keys())}")
        
        return next_node

    def run(self, shared_storage=None):
        """
        By default, do nothing (or raise).
        Subclasses (Flow, AsyncFlow) will implement.
        """
        raise NotImplementedError("BaseFlow.run must be implemented by subclasses")

    async def run_async(self, shared_storage=None):
        """
        By default, do nothing (or raise).
        Subclasses (Flow, AsyncFlow) will implement.
        """
        raise NotImplementedError("BaseFlow.run_async must be implemented by subclasses")

class Flow(BaseFlow):
    """
    Synchronous flow: each node is called with .run(shared_storage).
    """
    def _process_flow(self, shared_storage):
        current_node = self.start_node
        while current_node:
            # Pass down the Flow's parameters to the current node
            current_node.set_parameters(self.parameters)
            # Synchronous run
            condition = current_node.run(shared_storage)
            # Decide next node
            current_node = self.get_next_node(current_node, condition)

    def run(self, shared_storage=None):
        prep_result = self.preprocess(shared_storage)
        self._process_flow(shared_storage)
        return self.postprocess(shared_storage, prep_result, None)

class AsyncFlow(BaseFlow):
    """
    Asynchronous flow: if a node has .run_async, we await it.
    Otherwise, we fallback to .run.
    """
    async def _process_flow_async(self, shared_storage):
        current_node = self.start_node
        while current_node:
            current_node.set_parameters(self.parameters)

            # If node is async-capable, call run_async; otherwise run sync
            if hasattr(current_node, "run_async") and callable(current_node.run_async):
                condition = await current_node.run_async(shared_storage)
            else:
                condition = current_node.run(shared_storage)

            current_node = self.get_next_node(current_node, condition)

    async def run_async(self, shared_storage=None):
        prep_result = self.preprocess(shared_storage)
        await self._process_flow_async(shared_storage)
        return self.postprocess(shared_storage, prep_result, None)

    def run(self, shared_storage=None):
        return asyncio.run(self.run_async(shared_storage))
    
class BaseBatchFlow(BaseFlow):
    """
    Abstract base for a flow that runs multiple times (a batch),
    once for each set of parameters or items from preprocess().
    """
    def preprocess(self, shared_storage):
        """
        By default, returns an iterable of parameter-dicts or items
        for the flow to process in a batch.
        """
        return []

    def post_batch_run(self, all_results):
        """
        Hook for after the entire batch is done, to combine results, etc.
        """
        return all_results

class BatchFlow(BaseBatchFlow, Flow):
    """
    Synchronous batch flow: calls the flow repeatedly 
    for each set of parameters/items in preprocess().
    """
    def run(self, shared_storage=None):
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

        # Postprocess the entire batch
        result = self.post_batch_run(all_results)
        return self.postprocess(shared_storage, prep_result, result)

class BatchAsyncFlow(BaseBatchFlow, AsyncFlow):
    """
    Asynchronous batch flow: calls the flow repeatedly in an async manner
    for each set of parameters/items in preprocess().
    """
    async def run_async(self, shared_storage=None):
        prep_result = self.preprocess(shared_storage)
        all_results = []

        for param_dict in prep_result:
            original_params = self.parameters.copy()
            self.parameters.update(param_dict)

            await self._process_flow_async(shared_storage)

            all_results.append(f"Finished async run with parameters: {param_dict}")

            # Reset back to original parameters if needed
            self.parameters = original_params

        # Combine or process results at the end
        result = self.post_batch_run(all_results)
        return self.postprocess(shared_storage, prep_result, result)