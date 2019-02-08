import unittest
import chess

from state import State

class TestState(unittest.TestCase):

    def test_zero_state(self):
        zero_state = State(chess.Board())
        self.assertEqual(zero_state.value(), 0)

if __name__ == '__main__':
    unittest.main()
