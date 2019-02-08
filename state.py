import chess
import numpy as np

VALUES = {
        chess.PAWN:1,
        chess.KNIGHT:3,
        chess.BISHOP:3,
        chess.ROOK:5,
        chess.QUEEN:10,
        chess.KING:100 }

MAXVALUE = 100000
MINVALUE = -MAXVALUE

class State(object):
    """
    Simple class that take a board an turn it as a state. A State is like
    a node in a graph.
    """
    def __init__(self, board=None):

        # if board is none then we generate a new one
        if board is None:
            self._board = chess.Board()
        else:
            self._board = board

    def serialize(self):
        """
        This method return a 1*64 numpy array as a representation of the state
        It will be necessary for the NeuralNet
        """
        state = np.zeros(64, np.uint8)
        # TODO: Implement serialize method
        return state

    def edges(self):
        return list(self._board.legal_moves)

    def value(self):
        """
        Function that value a board.
        return: float
        """

        b = self._board
        # Check game over
        if b.is_game_over():
            #White win
            if b.result() == "1-0":
                return MAXVALUE
            elif b.result() == "0-1":
                return MINVALUE
            else:
                return 0

        value = 0

        # Compute board value
        pieces = b.piece_map()
        for i in pieces:
            pval = VALUES[pieces[i].piece_type]
            if pieces[i].color == chess.WHITE:
                value += pval
            else:
                value -= pval

        return value
