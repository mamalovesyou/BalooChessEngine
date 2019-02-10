# Simple server to play chess

import chess
from flask import Flask, Response, request
from state import State
from minmax import minmax_move

app = Flask("Chess Server app")

state = State()

@app.route("/")
def index():
    board = state.get_board()
    index = open("index.html").read()
    index.replace('zero_board', board.fen())
    return index

@app.route("/newgame")
def new_game():
    board = state.get_board()
    board.reset()
    response = app.response_class(response=board.fen(), status=200)
    return response

@app.route("/move")
def move():
    board = state.get_board()
    if not board.is_game_over():
        src = int(request.args.get('from', default=''))
        tgt = int(request.args.get('to', default=''))

        # Handle promotion case
        promotion_type = None
        if request.args.get('promotion', default='') == 'true' :
            promotion_symbol = request.args.get('promotion_symbol', default='')
            promotion_type = chess.Piece.from_symbol(promotion_symbol)

        next_move = board.san(chess.Move(src, tgt, promotion=promotion_type))
        if next_move is not None:
            board.push_san(next_move)
            ai_move = minmax_move(state)
            board.push(ai_move)

    response = app.response_class(response=board.fen(), status=200)
    return response


if __name__ == "__main__":
    app.run(debug=True)
