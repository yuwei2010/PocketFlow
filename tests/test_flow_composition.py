import unittest
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from minillmflow import Node, Flow

class NumberNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def process(self, shared_storage, prep_result):
        shared_storage['current'] = self.number

class AddNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def process(self, shared_storage, prep_result):
        shared_storage['current'] += self.number

class MultiplyNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def process(self, shared_storage, prep_result):
        shared_storage['current'] *= self.number


class TestFlowComposition(unittest.TestCase):

    def test_flow_as_node(self):
        """
        Demonstrates that a Flow can itself be chained like a Node.
        We create a flow (f1) that starts with NumberNode(5) -> AddNode(10).
        Then we chain f1 >> MultiplyNode(2).
        
        Expected result after running from f1:
          start = 5
          5 + 10 = 15
          15 * 2 = 30
        """
        shared_storage = {}

        # Inner flow f1
        f1 = Flow(start_node=NumberNode(5))
        f1 >> AddNode(10)

        # Then chain a node after the flow
        f1 >> MultiplyNode(2)

        # Run from f1
        f1.run(shared_storage)

        self.assertEqual(shared_storage['current'], 30)

    def test_nested_flow(self):
        """
        Demonstrates embedding one Flow inside another Flow.
        inner_flow: NumberNode(5) -> AddNode(3)
        outer_flow: starts with inner_flow -> MultiplyNode(4)
        
        Expected result:
          (5 + 3) * 4 = 32
        """
        shared_storage = {}
        
        # Define an inner flow
        inner_flow = Flow(start_node=NumberNode(5))
        inner_flow >> AddNode(3)

        # Define an outer flow, whose start node is inner_flow
        outer_flow = Flow(start_node=inner_flow)
        outer_flow >> MultiplyNode(4)

        # Run outer_flow
        outer_flow.run(shared_storage)

        self.assertEqual(shared_storage['current'], 32)  # (5+3)*4=32

    def test_flow_chaining_flows(self):
        """
        Demonstrates chaining one flow to another flow.
        flow1: NumberNode(10) -> AddNode(10)  # final shared_storage['current'] = 20
        flow2: MultiplyNode(2)               # final shared_storage['current'] = 40
        
        flow1 >> flow2 means once flow1 finishes, flow2 starts.
        
        Expected result: (10 + 10) * 2 = 40
        """
        shared_storage = {}

        # flow1
        flow1 = Flow(start_node=NumberNode(10))
        flow1 >> AddNode(10)

        # flow2
        flow2 = Flow(start_node=MultiplyNode(2))

        # Chain them: flow1 >> flow2
        flow1 >> flow2

        # Start running from flow1
        flow1.run(shared_storage)

        self.assertEqual(shared_storage['current'], 40)

    def test_flow_with_parameters(self):
        """
        Demonstrates passing parameters into a Flow (and retrieved by a Node).
        """

        class ParamNode(Node):
            def process(self, shared_storage, prep_result):
                # Reads 'level' from the node's (or flow's) parameters
                shared_storage['param'] = self.parameters.get('level', 'no param')

        shared_storage = {}

        # Create a flow with a ParamNode
        f = Flow(start_node=ParamNode())
        # Set parameters on the flow
        f.parameters = {'level': 'Level 1'}

        f.run(shared_storage)

        self.assertEqual(shared_storage['param'], 'Level 1')


if __name__ == '__main__':
    unittest.main()
