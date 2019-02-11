import time
import chess
from node import Node
from valuator import Valuator

class MinMax:

    DEFAULT_MAX_DEPTH = 4

    def __init__(self, max_depth=DEFAULT_MAX_DEPTH):
        self.max_depth = max_depth
        self.valuator = Valuator()

    def minmax(self, node, depth, alpha, beta):
        """
        AI function that choice the best move
        :param node: current node of the board
        :param depth: node index in the tree
        :param count: int that is the number of times the minmax func is called
        :return: best value depends of who's turn it is
        """
        b = node.board

        # check if depth is max depth or if game is over
        # then we return the value of the board
        if depth == self.max_depth or b.is_game_over():
            return self.valuator(b)

        if b.turn == chess.WHITE:
            best_val = self.valuator.MINVALUE
        else:
            best_val = self.valuator.MAXVALUE

        moves = []
        for m in node.edges():
            b.push(m)
            moves.append((m, self.valuator(b)))
            b.pop()
        sorted_moves = sorted(moves, key=lambda x:x[1], reverse=b.turn)


        # check value for each moves
        for m in [x[0] for x in sorted_moves]:

            b.push(m)
            tval = self.minmax(node, depth+1, alpha, beta)
            b.pop()

            # if it's white turn then your goal is to maximize
            if b.turn == chess.WHITE:
                best_val = max(best_val, tval)
                alpha = max(alpha, best_val)
                if (alpha <= beta):
                    return best_val

            # if it's black turn then you want to minimize
            else:
                best_val = min(best_val, tval)
                beta = min(best_val, beta)
                if (alpha >= beta):
                    return best_val

        return best_val

    def next_move(self, node):
        b = node.board
        depth = 0
        best_move = None
        self.valuator.reset()

        start = time.time()

        if b.turn == chess.WHITE:
            best_val = self.valuator.MINVALUE
        else:
            best_val = self.valuator.MAXVALUE

        for m in node.edges():
            b.push(m)
            tval = self.minmax(node, depth, self.valuator.MINVALUE,
                    self.valuator.MAXVALUE)
            b.pop()

            if b.turn == chess.WHITE:
                if tval >= best_val:
                    best_val = tval
                    best_move = m
            else:
                if tval <= best_val:
                    best_val = tval
                    best_move = m

        eta = time.time() - start
        print("Best value: %.2f -> %s : explored %d nodes in %.3f seconds" %
                (best_val, str(best_move), self.valuator.count, eta))

        return best_move


