import asyncio

# ---------------------------------------------------------------------
# Base Classes
# ---------------------------------------------------------------------
class BaseNode:
    def __init__(self):
        self.set_parameters({})
        self.successors = {}
        
    def set_parameters(self, parameters):
        self.parameters = parameters.copy() if parameters else {}
        
    def add_successor(self, node, condition="default"):
        self.successors[condition] = node
        return node
        
    async def preprocess(self, shared_storage):
        return None

    async def process_one(self, shared_storage, item):
        """
        The main single-item processing method that end developers override.
        Default does nothing.
        """
        return None

    async def robust_process_one(self, shared_storage, item):
        """
        In BaseNode, this is just a pass-through to `process_one`.
        Subclasses (like Node with retry) can override this to add extra logic.
        """
        return await self.process_one(shared_storage, item)

    async def process(self, shared_storage, preprocess_result):
        """
        Calls `robust_process_one` instead of `process_one` so that
        any subclass overrides of robust_process_one will apply.
        """
        return await self.robust_process_one(shared_storage, preprocess_result)
        
    async def postprocess(self, shared_storage, preprocess_result, process_result):
        return "default"
        
    async def run_one(self, shared_storage):
        preprocess_result = await self.preprocess(shared_storage)
        process_result = await self.process(shared_storage, preprocess_result)
        condition = await self.postprocess(shared_storage, preprocess_result, process_result)
        
        if not self.successors:
            return None
        elif len(self.successors) == 1:
            return next(iter(self.successors.values()))
        return self.successors.get(condition)

    def run(self, shared_storage=None):
        return asyncio.run(self.run_async(shared_storage))

    async def run_async(self, shared_storage=None):
        shared_storage = shared_storage or {}
        current_node = self
        while current_node:
            current_node = await current_node.run_one(shared_storage)
        
    def __rshift__(self, other):
        return self.add_successor(other)
    
    def __gt__(self, other):
        if isinstance(other, str):
            return _ConditionalTransition(self, other)
        elif isinstance(other, BaseNode):
            return self.add_successor(other)
        raise TypeError("Unsupported operand type")
    
    def __call__(self, condition):
        return _ConditionalTransition(self, condition)


class _ConditionalTransition:
    def __init__(self, source_node, condition):
        self.source_node = source_node
        self.condition = condition
    
    def __gt__(self, target_node):
        if not isinstance(target_node, BaseNode):
            raise TypeError("Target must be a BaseNode")
        return self.source_node.add_successor(target_node, self.condition)


# ---------------------------------------------------------------------
# Flow: allows you to define a "start_node" that is run in a sub-flow
# ---------------------------------------------------------------------
class Flow(BaseNode):
    def __init__(self, start_node=None):
        super().__init__()
        self.start_node = start_node
            
    async def process_one(self, shared_storage, item):
        # Instead of doing a single operation, we run a sub-flow
        if self.start_node:
            current_node = self.start_node
            while current_node:
                # Pass down the parameters
                current_node.set_parameters(self.parameters)
                current_node = await current_node.run_one(shared_storage or {})


# ---------------------------------------------------------------------
# Node: adds robust retry logic on top of BaseNode
# ---------------------------------------------------------------------
class Node(BaseNode):
    """
    Retries its single-item operation up to `max_retries` times,
    waiting `delay_s` seconds between attempts.
    By default: max_retries=5, delay_s=0.1
    End developers simply override `process_one` to define logic.
    """

    def __init__(self, max_retries=5, delay_s=0.1):
        super().__init__()
        self.parameters.setdefault("max_retries", max_retries)
        self.parameters.setdefault("delay_s", delay_s)

    async def fail_one(self, shared_storage, item, exc):
        """
        Called if the final retry also fails. By default,
        just returns a special string or could log an error.
        End developers can override this to do something else 
        (e.g., store the failure in a separate list or 
        trigger alternative logic).
        """
        # Example: log and return a special status
        print(f"[FAIL_ONE] item={item}, error={exc}")
        return "fail"

    async def robust_process_one(self, shared_storage, item):
        max_retries = self.parameters.get("max_retries", 5)
        delay_s = self.parameters.get("delay_s", 0.1)

        for attempt in range(max_retries):
            try:
                # Defer to the user's process_one logic
                return await super().robust_process_one(shared_storage, item)
            except Exception as e:
                if attempt == max_retries - 1:
                    # Final attempt failed; call fail_one
                    return await self.fail_one(shared_storage, item, e)
                # Otherwise, wait a bit and try again
                await asyncio.sleep(delay_s)

# ---------------------------------------------------------------------
# BatchMixin: processes a collection of items by calling robust_process_one for each
# ---------------------------------------------------------------------
class BatchMixin:
    async def process(self, shared_storage, items):
        """
        Processes a *collection* of items in a loop, calling robust_process_one per item.
        """
        partial_results = []
        for item in items:
            r = await self.robust_process_one(shared_storage, item)
            partial_results.append(r)
        return self.merge(shared_storage, partial_results)

    def merge(self, shared_storage, partial_results):
        """
        Combines partial results into a single output.
        By default, returns the list of partial results.
        """
        return partial_results

    async def preprocess(self, shared_storage):
        """
        Typically, you'd return a list or collection of items to process here.
        By default, returns an empty list.
        """
        return []


# ---------------------------------------------------------------------
# BatchNode: combines Node (robust logic) + BatchMixin (batch logic)
# ---------------------------------------------------------------------
class BatchNode(BatchMixin, Node):
    """
    A batch-processing node that:
      - Inherits robust retry logic from Node
      - Uses BatchMixin to process a list of items
    """

    async def preprocess(self, shared_storage):
        # Gather or return the batch items. By default, no items.
        return []

    async def process_one(self, shared_storage, item):
        """
        The per-item logic that the end developer will override.
        By default, does nothing.
        """
        return None


# ---------------------------------------------------------------------
# BatchFlow: combines Flow (sub-flow logic) + batch processing + robust logic
# ---------------------------------------------------------------------
class BatchFlow(BatchMixin, Flow):
    """
    This class runs a sub-flow (start_node) for each item in a batch.
    If you also want robust retries, you can adapt or combine with `Node`.
    """

    async def preprocess(self, shared_storage):
        # Return your batch items here
        return []

    async def process(self, shared_storage, items):
        """
        For each item, run the sub-flow (start_node).
        """
        results = []
        for item in items:
            # Here we re-run the sub-flow, which happens inside process_one of Flow
            await self.process_one(shared_storage, item)
            # Optionally collect results or do something after the sub-flow
            results.append(f"Finished sub-flow for item: {item}")
        return results