import asyncio, warnings

class BaseNode:
    def __init__(self): self.params, self.successors = {}, {}
    def set_params(self, params): self.params = params
    def add_successor(self, node, cond="default"):
        if cond in self.successors: warnings.warn(f"Overwriting existing successor for '{cond}'")
        self.successors[cond] = node; return node
    def preprocess(self, s): return None
    def process(self, s, p): return None
    def _process(self, s, p): return self.process(s, p)
    def postprocess(self, s, pr, r): return "default"
    def _run(self, s):
        pr = self.preprocess(s)
        r = self._process(s, pr)
        return self.postprocess(s, pr, r)
    def run(self, s):
        if self.successors: warnings.warn("Has successors; use Flow.run() instead.")
        return self._run(s)
    def __rshift__(self, other): return self.add_successor(other)
    def __sub__(self, cond):
        if isinstance(cond, str): return _ConditionalTransition(self, cond)
        raise TypeError("Condition must be a string")

class _ConditionalTransition:
    def __init__(self, src, c): self.src, self.c = src, c
    def __rshift__(self, tgt): return self.src.add_successor(tgt, self.c)

class Node(BaseNode):
    def __init__(self, max_retries=1): super().__init__(); self.max_retries = max_retries
    def process_after_fail(self, s, d, e): raise e
    def _process(self, s, d):
        for i in range(self.max_retries):
            try: return super()._process(s, d)
            except Exception as e:
                if i == self.max_retries - 1: return self.process_after_fail(s, d, e)

class BatchNode(Node):
    def preprocess(self, s): return []
    def process(self, s, item): return None
    def _process(self, s, items): return [super(Node, self)._process(s, i) for i in items]

class BaseFlow(BaseNode):
    def __init__(self, start_node): super().__init__(); self.start_node = start_node
    def get_next_node(self, curr, c):
        nxt = curr.successors.get(c)
        if nxt is None and curr.successors: warnings.warn(f"Flow ends. '{c}' not found in {list(curr.successors.keys())}")
        return nxt

class Flow(BaseFlow):
    def _process(self, s, p=None):
        curr, p = self.start_node, (p if p is not None else self.params.copy())
        while curr:
            curr.set_params(p)
            c = curr._run(s)
            curr = self.get_next_node(curr, c)
    def process(self, s, pr): raise NotImplementedError("Use Flow._process(...) instead")

class BaseBatchFlow(BaseFlow):
    def preprocess(self, s): return []

class BatchFlow(BaseBatchFlow, Flow):
    def _run(self, s):
        pr = self.preprocess(s)
        for d in pr:
            mp = self.params.copy(); mp.update(d)
            self._process(s, mp)
        return self.postprocess(s, pr, None)

class AsyncNode(Node):
    def postprocess(self, s, pr, r): raise NotImplementedError("Use postprocess_async")
    async def postprocess_async(self, s, pr, r): await asyncio.sleep(0); return "default"
    async def run_async(self, s):
        if self.successors: warnings.warn("Has successors; use AsyncFlow.run_async() instead.")
        return await self._run_async(s)
    async def _run_async(self, s):
        pr = self.preprocess(s)
        r = self._process(s, pr)
        return await self.postprocess_async(s, pr, r)
    def _run(self, s): raise RuntimeError("AsyncNode requires async execution")

class AsyncFlow(BaseFlow, AsyncNode):
    async def _process_async(self, s, p=None):
        curr, p = self.start_node, (p if p else self.params.copy())
        while curr:
            curr.set_params(p)
            c = await curr._run_async(s) if hasattr(curr, "run_async") else curr._run(s)
            curr = self.get_next_node(curr, c)
    async def _run_async(self, s):
        pr = self.preprocess(s)
        await self._process_async(s)
        return await self.postprocess_async(s, pr, None)

class BatchAsyncFlow(BaseBatchFlow, AsyncFlow):
    async def _run_async(self, s):
        pr = self.preprocess(s)
        for d in pr:
            mp = self.params.copy(); mp.update(d)
            await self._process_async(s, mp)
        return await self.postprocess_async(s, pr, None)