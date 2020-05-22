from pyca.universe1d import Universe1D
from pyca.rules.BaseRule import ClassicRule
from pyca.switch import ClassicSwitch1D
from pyca.observer import plot1d_universe

size = 600
switch = ClassicSwitch1D(rule_list=['01101110', '01101111'], window=50)
universe = Universe1D(size, apply_different_rule=True, switch=switch)
universe.register_cell_type(ClassicRule, 'single', pos=size-1, rule='01101110')
universe.initialize()
universe.compute(size)
plot1d_universe(universe)
