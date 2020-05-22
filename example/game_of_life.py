from pyca.universe2d import Universe2D
from pyca.celltype import GameOfLife
from pyca.observer import plot2d_animate

universe = Universe2D(50, 50)
universe.register_cell_type(GameOfLife, 'full_fill', life_prob=0.3)
universe.initialize()
universe.compute(500)
plot2d_animate(universe, write_to='../assets/game_of_life.gif')