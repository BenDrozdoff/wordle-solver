# Wordle Solver

A solver for wordle. The solver aims to get maximal information on each turn, usually via unguessed letters, until the number of candidates is fewer than the number of guesses remaining

## See optimal guesses in iPython

```python
from game import Game
Game("hello", verbose=True).play()
```
```
12972 possible words
Guess: slart
Results: ['missing', 'incorrect', 'missing', 'missing', 'missing']
499 possible words
Guess: decoy
Results: ['missing', 'correct', 'missing', 'incorrect', 'missing']
5 possible words
Guess: hoing
Results: ['correct', 'incorrect', 'missing', 'missing', 'missing']
1 possible words
Guess: hello
Results: ['correct', 'correct', 'correct', 'correct', 'correct']
Success in 4 guesses
```

## Statistics
`python simulate.py`
```
Success Rate: 0.991
Average Guesses: 4.297679112008073
Stdev Guesses: 0.813766230932009
Failing Words: ['tents', 'wowed', 'perps', 'bitty', 'fines', 'bells', 'peels', 'jests', 'oases']
```