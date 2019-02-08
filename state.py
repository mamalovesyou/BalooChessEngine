#!/usr/bin/env python3
import chess
import numpy as np


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
        """
        state = np.zeros(64, np.uint8)
        # TODO: Implement serialize method
        return state

    def edges(self):
        return list(self._board.legal_moves)


