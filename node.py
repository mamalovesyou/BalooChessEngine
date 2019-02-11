import chess
import numpy as np

class Node(object):
    """
    Simple class that represent a board in a game tree.
    """

    def __init__(self, board=None):
        # if board is none then we generate a new one
        if board is None:
            self.board = chess.Board()
        else:
            self.board = board

    def key(self):
        """
        Return a hash of the node
        """
        return hash((self.board.board_fen(), self.board.turn,
                self.board.castling_rights, self.board.ep_square))


    def serialize(self):
        """
        This method return a 1*64 numpy array as a representation of the state
        It will be necessary for the NeuralNet
        """
        state = np.zeros(64, np.uint8)
        # TODO: Implement serialize method
        return state

    def edges(self):
        """
        Compute all possible moves
        return: list of all possible moves
        """

        return list(self.board.legal_moves)


