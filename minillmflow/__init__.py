import asyncio

# ---------------------------------------------------------------------
# BaseNode (no duplication of run_one)
# ---------------------------------------------------------------------
class BaseNode:
    def __init__(self):
        self.parameters = {}
        self.successors = {}
        
    def add_successor(self, node, condition="default"):
        self.successors[condition] = node
        return node

    async def preprocess(self, shared_storage):
        """
        Override if needed to load or prepare data.
        """
        return None

    async def process(self, shared_storage, data):
        """
        Public method for user logic. Default does nothing.
        """
        return None

    async def _process(self, shared_storage, data):
        """
        Internal hook that calls `process(...)`.
        Subclasses override this to add extra logic (e.g. retries).
        """
        return await self.process(shared_storage, data)

    async def postprocess(self, shared_storage, preprocess_result, process_result):
        """
        By default, returns "default" to pick the default successor.
        """
        return "default"
        
    async def run_one(self, shared_storage):
        """
        One cycle of the node:
          1) preprocess
          2) _process
          3) postprocess
          4) pick successor
        """
        preprocess_result = await self.preprocess(shared_storage)
        process_result = await self._process(shared_storage, preprocess_result)
        condition = await self.postprocess(shared_storage, preprocess_result, process_result)
        
        if not self.successors:
            return None
        if len(self.successors) == 1:
            return next(iter(self.successors.values()))
        return self.successors.get(condition)

    def run(self, shared_storage=None):
        return asyncio.run(self.run_async(shared_storage))

    async def run_async(self, shared_storage=None):
        shared_storage = shared_storage or {}
        current_node = self
        while current_node:
            current_node = await current_node.run_one(shared_storage)
        
    # Syntactic sugar for chaining
    def __rshift__(self, other):
        return self.add_successor(other)
    
    def __gt__(self, other):
        """
        For branching: node > "condition" > another_node
        """
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


class Node(BaseNode):
    """
    Single-item node with robust logic. 
    End devs override `process(...)`. 
    `_process(...)` adds the retry logic.
    """
    def __init__(self, max_retries=5, delay_s=0.1):
        super().__init__()
        self.max_retries = max_retries
        self.delay_s = delay_s

    async def fail_item(self, shared_storage, data, exc):
        """
        Called if we exhaust all retries. 
        """
        print(f"[FAIL_ITEM] data={data}, error={exc}")
        return "fail"

    async def _process(self, shared_storage, data):
        """
        Wraps the user’s `process(...)` with retry logic.
        """
        for attempt in range(self.max_retries):
            try:
                return await super()._process(shared_storage, data)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return await self.fail_item(shared_storage, data, e)
                await asyncio.sleep(self.delay_s)

# ---------------------------------------------------------------------
# BatchNode: processes multiple items
# ---------------------------------------------------------------------
class BatchNode(BaseNode):
    """
    Processes a list of items in `process(...)`.
    The user overrides `process_one(item)`.
    `_process_one(...)` handles robust retries for each item.
    """

    def __init__(self, max_retries=5, delay_s=0.1):
        super().__init__()
        self.max_retries = max_retries
        self.delay_s = delay_s

    async def preprocess(self, shared_storage):
        """
        Typically return a list of items to process.
        """
        return []

    async def process_one(self, shared_storage, item):
        """
        End developers override single-item logic here.
        """
        return None

    async def _process_one(self, shared_storage, item):
        """
        Retry logic around process_one(item).
        """
        for attempt in range(self.max_retries):
            try:
                return await self.process_one(shared_storage, item)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    print(f"[FAIL_ITEM] item={item}, error={e}")
                    return "fail"
                await asyncio.sleep(self.delay_s)

    async def _process(self, shared_storage, items):
        """
        Loops over items, calling _process_one per item.
        """
        results = []
        for item in items:
            r = await self._process_one(shared_storage, item)
            results.append(r)
        return results


class Flow(BaseNode):
    """
    Runs a sub-flow from `start_node` once per call.
    """
    def __init__(self, start_node=None):
        super().__init__()
        self.start_node = start_node

    async def _process(self, shared_storage, _):
        if self.start_node:
            current_node = self.start_node
            while current_node:
                current_node = await current_node.run_one(shared_storage or {})
        return "Flow done"

class BatchFlow(BaseNode):
    """
    For each param_dict in the batch, merges it into self.parameters,
    then runs the sub-flow from `start_node`.
    """

    def __init__(self, start_node=None):
        super().__init__()
        self.start_node = start_node

    async def preprocess(self, shared_storage):
        """
        Return a list of param_dict objects.
        """
        return []

    async def process_one(self, shared_storage, param_dict):
        """
        Merge param_dict into the node's parameters,
        then run the sub-flow.
        """
        node_parameters = self.parameters.copy()
        node_parameters.update(param_dict)

        if self.start_node:
            current_node = self.start_node
            while current_node:
                # set the combined parameters
                current_node.set_parameters(node_parameters)
                current_node = await current_node.run_one(shared_storage or {})

    async def _process(self, shared_storage, items):
        """
        For each param_dict in items, run the sub-flow once.
        """
        results = []
        for param_dict in items:
            await self.process_one(shared_storage, param_dict)
            results.append(f"Ran sub-flow for param_dict={param_dict}")
        return results