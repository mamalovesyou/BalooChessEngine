import chess

class Valuator:
    """
    Simple value function that value a board
    """

    PIECES_VALUES = {
        chess.PAWN:1,
        chess.KNIGHT:3,
        chess.BISHOP:3,
        chess.ROOK:5,
        chess.QUEEN:10,
        chess.KING:100 }

    MAXVALUE = 100000
    MINVALUE = -MAXVALUE


    def __init__(self):
        self.count = 0

    def __call__(self, node):
        """
        Each time Valuator is called, we increment counter
        node: chess board node
        return: value of the node (chess board)
        """

        self.count += 1
        return self.value(node)

    def value(self, node):
        """
        Function that value a board.
        node: chess board node
        return: float
        """

        # Check game over
        if node.board.is_game_over():
            #White win
            if node.board.result() == "1-0":
                return self.MAXVALUE
            elif node.board.result() == "0-1":
                return self.MINVALUE
            else:
                return 0

        value = 0

        # Compute board value
        pieces = node.board.piece_map()
        for i in pieces:
            pval = self.PIECES_VALUES[pieces[i].piece_type]
            if pieces[i].color == chess.WHITE:
                value += pval
            else:
                value -= pval

        return value

    def reset(self):
        """
        Reset counter
        """

        self.count = 0
