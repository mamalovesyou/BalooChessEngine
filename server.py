# Simple server to play chess

import chess
import traceback
from flask import Flask, Response, request
from node import Node
from minmax import MinMax
from valuator import Valuator

app = Flask("Chess Server app")

node = Node()
valuator = Valuator()
minmax = MinMax(max_depth=3, valuator=valuator)

@app.route("/")
def index():
    board = node.board
    index = open("index.html").read()
    index.replace('zero_board', board.fen())
    return index

@app.route("/newgame")
def new_game():
    board = node.board
    board.reset()
    valuator.reset()
    response = app.response_class(response=board.fen(), status=200)
    return response

@app.route("/move")
def move():
    board = node.board
    if not board.is_game_over():
        src = int(request.args.get('from', default=''))
        tgt = int(request.args.get('to', default=''))

        # Handle promotion case
        promotion_symbol = None
        if request.args.get('promotion', default='') == 'true' :
            promotion_symbol = request.args.get('promotion_symbol', default='')

        next_move = board.san(chess.Move(src, tgt, promotion=promotion_symbol))

        if next_move is not None:
            try:
                board.push_san(next_move)
                ai_move = minmax.next_move(node)
                board.push(ai_move)
            except:
                traceback.print_exc()

    response = app.response_class(response=board.fen(), status=200)
    return response


if __name__ == "__main__":
    app.run(debug=True)

