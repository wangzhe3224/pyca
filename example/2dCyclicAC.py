from pyca.universe2d import Universe2D
from pyca.rules.Cyclic2D import Cyclic2D
from pyca.observer import plot2d_animate, plot2d_universe

universe = Universe2D(100, 100)
universe.register_cell_type(Cyclic2D, 'whatever..we only have one fill strategy for now..',
                            # These are the setup for cell
                            random=True, max_states=16, threshold=1, level=1)
universe.initialize()
universe.compute(1000)
plot2d_animate(universe, write_to='../assets/2d_cyclic_ac.gif', color='RdPu', show=False)
