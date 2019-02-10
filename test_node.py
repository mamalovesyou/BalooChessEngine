import unittest
import chess

from node import Node

class TestNode(unittest.TestCase):

    def test_zero_node(self):
        zero_node = Node(chess.Board())
        self.assertEqual(zero_node.value(), 0)

if __name__ == '__main__':
    unittest.main()
