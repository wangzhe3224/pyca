# pyca

Cellular Automata, CA, in Python.

## Concepts

- Universe, contains all the cells, and function to trigger computation
- CellType, rule of the cell is defined here
- observer, way to observe universe

Currently, 2 2D universe is supported, you can define a CA by injecting a 
new type of CellType. 

## Examples:

### Game of Life

https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

[Code](./example/game_of_life.py)

![A random game of life](./assets/game_of_life.gif)
