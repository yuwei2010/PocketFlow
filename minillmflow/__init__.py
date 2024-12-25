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
        if not shared_storage:
            shared_storage = {}

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
                
class InteractiveNode(BaseNode):
    """
    Interactive node. Instead of returning a condition,
    we 'signal' the condition via a callback provided by the Flow.
    """

    def postprocess(self, shared_storage, prep_result, proc_result, next_node_callback):
        """
        We do NOT return anything. We call 'next_node_callback("some_condition")'
        to tell the Flow which successor to pick.
        """
        # e.g. here we pick "default", but in real usage you'd do logic or rely on user input
        next_node_callback("default")

    def run(self, shared_storage=None):
        """
        Run just THIS node (no chain).
        """
        if not shared_storage:
            shared_storage = {}

        # 1) Preprocess
        prep = self.preprocess(shared_storage)

        # 2) Process
        proc = self._process(shared_storage, prep)

        # 3) Postprocess with a dummy callback
        def dummy_callback(condition="default"):
            print("[Dummy callback] To run the flow, pass this node into a Flow instance.")
            
        self.postprocess(shared_storage, prep, proc, dummy_callback)
        
    def is_interactive(self):
        return True
      
class Flow:
    """
    A Flow that runs through a chain of nodes, from a start node onward.
    Each iteration:
      - preprocess
      - process
      - postprocess
    The postprocess is given a callback to choose the next node.
    We'll 'yield' the current node each time, so the caller can see progress.
    """
    def __init__(self, start_node=None):
        self.start_node = start_node

    def run(self, shared_storage=None):
        if shared_storage is None:
            shared_storage = {}

        current_node = self.start_node
        print("hihihi")
        
        while current_node:
            # 1) Preprocess
            prep_result = current_node.preprocess(shared_storage)
            print("prep")
            # 2) Process
            proc_result = current_node._process(shared_storage, prep_result)

            # Prepare next_node variable
            next_node = [None]

            # We'll define a callback only if this is an interactive node.
            # The callback sets next_node[0] based on condition.
            def next_node_callback(condition="default"):
                nxt = current_node.successors.get(condition)
                next_node[0] = nxt

            # 3) Check if it's an interactive node
            is_interactive = (
                hasattr(current_node, 'is_interactive') 
                and current_node.is_interactive()
            )

            if is_interactive:
                print("ineractive")
                #
                # ---- INTERACTIVE CASE ----
                #
                # a) yield so that external code can do UI, etc.
                # yield current_node, prep_result, proc_result, next_node_callback

                # # b) Now we do postprocess WITH the callback:
                # current_node.postprocess(
                #     shared_storage,
                #     prep_result,
                #     proc_result,
                #     next_node_callback
                # )
                # # once postprocess is done, next_node[0] should be set

            else:
                #
                # ---- NON-INTERACTIVE CASE ----
                #
                # We just call postprocess WITHOUT callback, 
                # and let it return the condition string:
                condition = current_node.postprocess(
                    shared_storage, 
                    prep_result, 
                    proc_result
                )
                # Then we figure out the next node:
                next_node[0] = current_node.successors.get(condition, None)

            # 5) Move on to the next node
            current_node = next_node[0]
            
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