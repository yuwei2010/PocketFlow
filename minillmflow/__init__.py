import asyncio

class BaseNode:
    def __init__(self):
        self.set_parameters({})  # immutable during processing; could be overwritten as node can be reused
        self.successors = {}
        
    def set_parameters(self, parameters):
        self.parameters = parameters.copy() if parameters else {}
        
    def add_successor(self, node, condition="default"):
        self.successors[condition] = node
        return node
        
    async def preprocess(self, shared_storage):
        return None
    
    async def process_one(self, shared_storage, item):
        return None
    
    async def process(self, shared_storage, preprocess_result):
        return await self.process_one(shared_storage, preprocess_result)
        
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

class BaseSuperNode(BaseNode):
    def __init__(self, start_node=None):
        super().__init__()
        self.start_node = start_node
            
    async def process_one(self, shared_storage, item):
        if self.start_node:
            current_node = self.start_node
            while current_node:
                current_node.set_parameters(self.parameters)
                current_node = await current_node.run_one(shared_storage or {})

class BatchMixin:
    async def process(self, shared_storage, items):
        partial_results = []
        for item in items:
            r = await self.process_one(shared_storage, item)
            partial_results.append(r)

        return self.merge(shared_storage, partial_results)

    def merge(self, shared_storage, partial_results):
        return partial_results

    async def preprocess(self, shared_storage):
        return []
    
class BatchBaseNode(BatchMixin, BaseNode):
    async def preprocess(self, shared_storage):
        return []
    
    async def process_one(self, shared_storage, item):
        return None

class BatchSuperNode(BatchMixin, BaseSuperNode):
    async def preprocess(self, shared_storage):
        return []
    
    async def process_one(self, shared_storage, param_dict):
        node_parameters = self.parameters.copy()
        node_parameters.update(param_dict)

        if self.start_node:
            current_node = self.start_node
            while current_node:
                current_node.set_parameters(node_parameters)
                current_node = await current_node.run_one(shared_storage or {})

