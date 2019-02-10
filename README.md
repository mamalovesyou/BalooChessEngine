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

#### MinMax

The general idea of minmax algorithm is to search among a tree of all possible games state,
evaluate them and choose a path to the win node. It seems to be simple, but with chess
we can't afford to evaluate every possible result for every possible moves. So we have to
defined how much moves ahead we want to evaluate. Maybe 3 or 4 would be enough. We also
have to keep in mind that we need our algorithm to not be so slow.

Note:
    After having a functional minmax search with a depth of 4, it take way too long to find a move.
    So For now, I'm gonna switch max depth to 3. Next step is to have a game server so that I can
    play against the computer.


### Todo

    - [x] Implement a Node class (Chess as Graph)
    - [x] Implement minmax algorithm
        - [ ] A&B Pruning
        - [ ] Better value function

    - [ ] Implement game server
    - [ ] Implement a simple NeuralNet
    - [ ] Implement a Convultional NeuralNet
