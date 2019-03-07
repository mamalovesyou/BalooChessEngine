# BalooChessEngine

Simple chess engine which implement different way to play.
    - using minmax approach
    - using neuralnet approach


### Installation
To install BalooChessEngine use a python3 virtualenv
```sh
$ pip3 install virtualenv
$ virtualenv BalooChessEnv
$ source BalooChessEnv/bin/activate
$ pip install -r requirement.txt
```

To exit your virtual env, use this command:
```sh
$ deactivate
```

### Implementation

#### MinMax Approach

The general idea of minmax algorithm is to search among a tree of all possible games state,
evaluate them and choose a path to the win node. It seems to be simple, but with chess
we can't afford to evaluate every possible result for every possible moves. So we have to
defined how much moves ahead we want to evaluate. Maybe 3 or 4 would be enough. We also
have to keep in mind that we need our algorithm to not be so slow.

Note:
    After having a functional minmax search with a depth of 4, it take way too long to find a move.
    I switched max depth to 3. Next step is to have a game server so that I can
    play against the computer.

Now I got a cool game server so I can play through my browser. But the AI still need at least 40s to make
it first move so let's improve it with the Alpha Beta pruning technic. The alpha-beta pruning is based on
the situation where we can stop evaluating a part of the search tree if we find a move that leads to a
worse situation than a previously discovered move. The alpha-beta pruning does not
influence the outcome of the minimax algorithm — it only makes it faster.

Note:
    The AI is much faster! Disclaimer: It still not that smart and easy to defeat.
    Next step is to improve the value function. A good start for that is [here](https://www.chessprogramming.org/Simplified_Evaluation_Function)


#### Neural Net Approach

##### Processing the data
The first step is to grab some data. Usualy chess game data are in the PGN format (Portable Game Notation).




### Todo

    - [x] Implement a Node class (Chess as Graph)

    - [x] Write a value function
        - [ ] Add more tests for the value function

    - [x] Implement minmax algorithm
        - [x] Add Alpha-Beta Pruning
        - [x] Add Piece Square Tables feature
        - [x] Add Legal moves count feature
        - [ ] Add Quiescence Search

    - [x] Build a dataset
        - [x] Process PGN Data
        - [x] Add Multiprocessing

    - [ ] Implement a Neural Net
        - [ ] Add a board to array converter
        - [ ] Implement

    - [x] Implement game server
        - [ ] Add more design
        - [ ] Add time took by AI
        - [ ] Add AI type choice

    - [ ] Implement a Convultional NeuralNet
