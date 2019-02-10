import time
import chess
from state import State, MINVALUE, MAXVALUE

MAX_DEPTH = 3

def minmax(state, depth, count):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree
    :param count: int that is the number of times the minmax func is called
    :return: best value depends of who's turn it is
    """
    b = state.get_board()
    count += 1

    # check if depth is max depth or if game is over
    # then we return the value of the board
    if depth == MAX_DEPTH or b.is_game_over():
        return state.value()

    if b.turn == chess.WHITE:
        best_val = MINVALUE
    else:
        best_val = MAXVALUE

    # check value for each moves
    for m in state.edges():
        b.push(m)
        tval = minmax(state, depth+1, count)
        b.pop()

        # if it's white turn then your goal is to maximize
        if b.turn == chess.WHITE:
            best_val = max(best_val, tval)
        # if it's black turn then you want to minimize
        else:
            best_val = min(best_val, tval)

    return best_val

def search_best_move(state):
    start = time.time()

    b = state.get_board()
    depth = 0
    count = 0
    best_move = None

    if b.turn == chess.WHITE:
        best_val = MINVALUE
    else:
        best_val = MAXVALUE

    for m in state.edges():
        b.push(m)
        tval = minmax(state, depth, count)
        print(tval, m)
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
            (best_val, str(best_move), count, eta))


if __name__ == "__main__":
    state = State()
    search_best_move(state)


