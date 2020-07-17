from pyca.universe1d import Universe1D
from pyca.rules.BaseRule import ClassicRule
from pyca.observer import plot1d_universe, plot1d_animate
from multiprocessing import Pool


def generate(param):
    rule, name = param
    print('Processing {}'.format(rule))
    size = 400
    universe = Universe1D(size)
    universe.register_cell_type(ClassicRule, 'single', pos=int(size/2), rule=rule)
    universe.initialize()
    universe.compute(size)
    plot1d_universe(universe, write_to='../assets/255/{}.png'.format(name), is_show=False)
    # plot1d_animate(universe, write_to='../assets/{}_animtion.gif'.format(rule))


rules = []
for i in range(256):
    rule = "{0:b}".format(i).rjust(8, '0')
    rules.append((rule, '{}_{}'.format(rule, i)))

# export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
# For mac to pool thread
with Pool(20) as p:
    p.map(generate, rules)
