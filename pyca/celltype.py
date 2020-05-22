from abc import ABC, abstractmethod
from typing import List

import numpy as np


class CellType(ABC):
    """ A cell type """

    @abstractmethod
    def neighbour_level(self) -> (int, int):
        """ return how many layers of neighbours to get """

    @abstractmethod
    def status(self) -> float:
        """ get cell status represented by integer """

    @abstractmethod
    def process(self, neighbours, cell_loc: (int, int)) -> float:
        """ process the cell given neighbours, return next status code as int """

    @abstractmethod
    def reset(self) -> float:
        """ reset cell to its initial status, return the status code """

    def __call__(self, *args, **kwargs):
        """ for the sake of pycharm... """
        self.__call__(*args, **kwargs)


class GameOfLife(CellType):
    """"""

    def __init__(self, **kwargs):
        is_live = kwargs.pop('is_live', 0.0)
        live_prob = kwargs.pop('life_prob', None)
        if live_prob is not None:
            self.state = np.random.choice([0, 1], p=[1-live_prob, live_prob])
        else:
            self.state = is_live

    def neighbour_level(self) -> (int, int):
        """ how many level neighbour to process """
        return 1, 1

    def status(self) -> float:
        return self.state

    def process(self, neighbours, cell_loc: (int, int)) -> float:
        """ process status of the cell

        Rules:
        1. less than 2 living neighbours, die
        2. 2 or 3, live
        3. > 3, die
        4. a die cell, if =3, live

        :param neighbours: a matrix of neighbour including cell itself
        :param cell_loc: the loc of cell itself in neighbour
        :return:
        """
        counter = neighbours.sum() - self.state  # remove itself count
        # print(neighbours, counter, self.state)
        if self.state == 0.0:
            if counter == 3:
                self.state = 1.0  # rule 4
        else:
            if counter < 2:
                self.state = 0.0  # rule 1
            elif counter > 3:
                self.state = 0.0  # rule 3
            else:
                self.state = 1.0  # rule 2
        # print(self.state)
        return self.state

    def reset(self) -> float:
        self.state = 0.
        return self.state

