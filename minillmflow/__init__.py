import asyncio

def _wrap_async(fn):
    """
    Given a synchronous function fn, return a coroutine (async function) that
    simply awaits the (synchronous) call.
    """
    async def _async_wrapper(self, *args, **kwargs):
        return fn(self, *args, **kwargs)
    return _async_wrapper


class NodeMeta(type):
    """
    Metaclass that converts certain methods into async if they are not already.
    """
    def __new__(mcs, name, bases, attrs):
        # Add ANY method names you want to auto-wrap here:
        methods_to_wrap = (
            "preprocess",
            "process",
            "postprocess",
            "process_after_fail",
            "process_one",
            "process_one_after_fail",
        )

        for attr_name in methods_to_wrap:
            if attr_name in attrs:
                # If it's not already a coroutine function, wrap it
                if not asyncio.iscoroutinefunction(attrs[attr_name]):
                    old_fn = attrs[attr_name]
                    attrs[attr_name] = _wrap_async(old_fn)
        
        return super().__new__(mcs, name, bases, attrs)
    
class BaseNode(metaclass=NodeMeta):
    def __init__(self):
        self.parameters = {}
        self.successors = {}

    # By default these are already async. If a subclass overrides them
    # with non-async definitions, they'll get wrapped automatically.
    def preprocess(self, shared_storage):
        return None

    def process(self, shared_storage, data):
        return None

    def postprocess(self, shared_storage, preprocess_result, process_result):
        return "default"

    async def _process(self, shared_storage, data):
        return await self.process(shared_storage, data)

    async def _run_one(self, shared_storage):
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
            current_node = await current_node._run_one(shared_storage)

    # Syntactic sugar for chaining
    def add_successor(self, node, condition="default"):
        self.successors[condition] = node
        return node

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


class Node(BaseNode):
    def __init__(self, max_retries=5, delay_s=0.1):
        super().__init__()
        self.max_retries = max_retries
        self.delay_s = delay_s

    def process_after_fail(self, shared_storage, data, exc):
        print(f"[FAIL_ITEM] data={data}, error={exc}")
        return "fail"

    async def _process(self, shared_storage, data):
        for attempt in range(self.max_retries):
            try:
                return await super()._process(shared_storage, data)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return await self.process_after_fail(shared_storage, data, e)
                await asyncio.sleep(self.delay_s)

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

class Flow(BaseNode):
    def __init__(self, start_node=None):
        super().__init__()
        self.start_node = start_node

    async def _process(self, shared_storage, _):
        if self.start_node:
            current_node = self.start_node
            while current_node:
                current_node = await current_node._run_one(shared_storage or {})
        return "Flow done"

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