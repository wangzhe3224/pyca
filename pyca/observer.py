""" observe the steps of universe """
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from pyca.universe1d import Universe1D
from pyca.universe2d import Universe2D


def plot2d_animate(universe, title='', write_to:str=None, color='Greys', show=True):
    cmap = plt.get_cmap(color)
    fig = plt.figure()
    plt.title(title)
    im = plt.imshow(universe[0], animated=True, cmap=cmap)
    i = {'index': 0}
    def updatefig(*args):
        i['index'] += 1
        if i['index'] == len(universe):
            i['index'] = 0
        im.set_array(universe[i['index']])
        return im,
    ani = animation.FuncAnimation(fig, updatefig, interval=100, blit=True)
    if write_to is not None:
        ani.save(write_to, writer='imagemagick', fps=30)
    if show:
        plt.show()


def plot1d_animate(universe: Universe1D, title='', write_to:str=None, color='Greys', show=True):
    """ plot 1d universe compute """
    ims = universe.form_step_matrix()
    cmap = plt.get_cmap(color)
    fig = plt.figure()
    plt.title(title)
    im = plt.imshow(ims[0], animated=True, cmap=cmap)
    i = {'index': 0}
    def updatefig(*args):
        i['index'] += 1
        if i['index'] == len(universe):
            i['index'] = 0
        im.set_array(ims[i['index']])
        return im,
    ani = animation.FuncAnimation(fig, updatefig, interval=100, blit=True)
    if write_to is not None:
        ani.save(write_to, writer='imagemagick', fps=30)
    if show:
        plt.show()


def plot2d_universe(universe: Universe2D, step=-1, title=''):
    matrix = universe[step]
    cmap = plt.get_cmap('Blues')
    fig = plt.figure()
    plt.title(title)
    im = plt.imshow(matrix, animated=False, cmap=cmap)

    plt.show()


def plot1d_universe(universe: Universe1D, title='', write_to=''):
    cmap = plt.get_cmap('Greys')
    fig = plt.figure()
    plt.title(title)
    im = plt.imshow(universe.form_matrix(), animated=True, cmap=cmap)
    plt.show()
    if write_to:
        plt.savefig(write_to)