import unittest
import chess
from valuator import Valuator
from node import Node

class TestValuator(unittest.TestCase):

    def test_zero_board(self):
        node = Node()
        valuator = Valuator()
        material_val = valuator.get_material_value(node.board)
        square_val_w = valuator.get_all_masks_value(node.board, chess.WHITE)
        square_val_b = valuator.get_all_masks_value(node.board, chess.BLACK)

        self.assertEqual(material_val, 0)
        self.assertEqual(square_val_w + square_val_b, 0)




if __name__ == '__main__':
    unittest.main()
