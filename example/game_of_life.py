from pyca.universe2d import Universe2D
from pyca.celltype import GameOfLife
from pyca.observer import plot2d_animate

universe = Universe2D(100, 100)
universe.register_cell_type(GameOfLife, 'full_fill', life_prob=0.5)
universe.initialize()
universe.compute(500)
# plot2d_animate(universe, write_to='../assets/game_of_life.gif')
plot2d_animate(universe, show=True)