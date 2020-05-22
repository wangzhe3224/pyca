from pyca.universe1d import Universe1D
from pyca.rules.Rules import Rule30
from pyca.observer import plot1d_universe

universe = Universe1D(300)
universe.register_cell_type(Rule30, 'random', prob=0.5)
universe.initialize()
universe.compute(300)
plot1d_universe(universe)