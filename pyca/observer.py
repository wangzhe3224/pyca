""" observe the steps of universe """
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def plot2d_animate(universe, title='', write_to:str=None):
    cmap = plt.get_cmap('Greys')
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
    ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)
    if write_to is not None:
        ani.save(write_to, writer='imagemagick', fps=30)
    plt.show()