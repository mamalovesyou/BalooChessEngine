import chess

class Valuator:
    """
    Simple value function that value a board
    """

    PIECES_VALUES = {
        chess.PAWN:100,
        chess.KNIGHT:320,
        chess.BISHOP:330,
        chess.ROOK:500,
        chess.QUEEN:900,
        chess.KING:20000 }

    PIECES_SQUARE_VALUES = {
        chess.PAWN: [0, 0, 0, 0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10, 5, 5, 10, 25, 25, 10, 5, 5, 0, 0,
            0, 20, 20, 0, 0, 0, 5, -5,-10, 0, 0,-10, -5, 5, 5, 10, 10,-20,-20,
            10, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0],
        chess.KNIGHT: [-50,-40,-30,-30,-30,-30,-40,-50, -40,-20, 0, 0, 0,
            0,-20,-40, -30, 0, 10, 15, 15, 10, 0,-30, -30, 5, 15, 20, 20, 15,
            5,-30, -30, 0, 15, 20, 20, 15, 0,-30, -30, 5, 10, 15, 15, 10,
            5,-30, -40,-20, 0, 5, 5, 0,-20,-40, -50,-40,-30,-30,-30,-30,-40,-50],
        chess.QUEEN: [-20,-10,-10, -5, -5,-10,-10,-20, -10, 0, 0, 0, 0, 0,
            0,-10, -10, 0, 5, 5, 5, 5, 0,-10, -5, 0, 5, 5, 5, 5, 0, -5, 0, 0,
            5, 5, 5, 5, 0, -5, -10, 5, 5, 5, 5, 5, 0,-10, -10, 0, 5, 0, 0, 0,
            0,-10, -20,-10,-10, -5, -5,-10,-10,-20],
        chess.BISHOP: [-20,-10,-10,-10,-10,-10,-10,-20, -10, 0, 0, 0, 0, 0,
            0,-10, -10, 0, 5, 10, 10, 5, 0,-10, -10, 5, 5, 10, 10, 5, 5,-10,
            -10, 0, 10, 10, 10, 10, 0,-10, -10, 10, 10, 10, 10, 10, 10,-10,
            -10, 5, 0, 0, 0, 0, 5,-10, -20,-10,-10,-10,-10,-10,-10,-20],
        chess.ROOK: [0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 10, 10, 10, 10, 10, 5, -5,
            0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0,
            0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, 0, 0, 0,
            5, 5, 0, 0, 0],
        chess.KING: [-30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30, -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10, 20, 20, 0, 0, 0, 0, 20, 20, 20,
            30, 10, 0, 0, 10, 30, 20]}

    MAXVALUE = 100000
    MINVALUE = -MAXVALUE


    def __init__(self):
        self.count = 0

    def __call__(self, board):
        """
        Each time Valuator is called, we increment counter
        board: chess board
        return: value of the board
        """

        self.count += 1
        return self.value(board)


    def _get_material_value(self, board):
        """
        This function compute the material value of a board
        board: chhess.Board
        return: float
        """
        value = 0
        pieces = board.piece_map()
        for i in pieces:
            pval = self.PIECES_VALUES[pieces[i].piece_type]
            if pieces[i].color == chess.WHITE:
                value += pval
            else:
                value -= pval

        return value


    def _get_mask_value(self, board, piece_type, color):
        """
        Basicaly this function will give us a value depends on pieces position
        This feature is called Piece-Square Tables estimation
        piece_type: type of piece
        color: chess.WHITE or chess.BLACK

        return: computed value for a board
        """
        val = 0
        indexes = list(board.pieces(piece_type, color))
        for idx in indexes:
            mask = self.PIECES_SQUARE_VALUES[piece_type]
            if color == chess.BLACK:
                mask.reverse()
            val += mask[idx]

        return val

    def _get_all_masks_value(self, board, color):
        """
        Compute value mask value for all pieces type
        color: chess.WHITE or chess.BLACK

        return: computed value for a board
        """
        val = 0
        for p in self.PIECES_SQUARE_VALUES.keys():
            val += self._get_mask_value(board, p, color)
        return val

    def value(self, board):
        """
        Function that value a board.
        board: chess board
        return: float
        """

        # Check game over
        if board.is_game_over():
            #White win
            if board.result() == "1-0":
                return self.MAXVALUE
            elif board.result() == "0-1":
                return self.MINVALUE
            else:
                return 0

        value = 0
        value += self._get_material_value(board)
        value += self._get_all_masks_value(board, board.turn)


        return value

    def reset(self):
        """
        Reset counter
        """
        self.count = 0
