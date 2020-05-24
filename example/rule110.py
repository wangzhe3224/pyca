from pyca.universe1d import Universe1D
from pyca.rules.BaseRule import ClassicRule
from pyca.observer import plot1d_universe, plot1d_animate

size = 100
universe = Universe1D(size)
universe.register_cell_type(ClassicRule, 'single', pos=size-1, rule='01101110')
universe.initialize()
universe.compute(size)
# plot1d_universe(universe)
plot1d_animate(universe, write_to='../assets/rule110_animtion.gif')