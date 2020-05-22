import numpy as np
from pyca.celltype import CellType


class Cyclic2D(CellType):
    """
    As with any cellular automaton, the cyclic cellular automaton consists of a regular grid of cells
     in one or more dimensions. The cells can take on any of {\displaystyle n}n states,
     ranging from {\displaystyle 0}{\displaystyle 0} to {\displaystyle n-1}n-1. The first
     generation starts out with random states in each of the cells. In each subsequent generation,
      if a cell has a neighboring cell whose value is the successor of the cell's value,
      the cell is "consumed" and takes on the succeeding value.
      (Note that {\displaystyle 0}{\displaystyle 0} is the successor of {\displaystyle n-1}n-1; see also modular arithmetic.)
      More general forms of this type of rule also include a threshold parameter, and only allow a cell to be
      consumed when the number of neighbors with the successor value exceeds this threshold.
    """

    def __init__(self, **kwargs):
        """

        Parameters
        ----------
        level: Optional, search level of neighbours
        max_states: Optional
        threshold: Optional
        init_state: Optional
        random: Optional, True
        """
        self.level = kwargs.pop('level', 1)
        self.max_states = kwargs.pop('max_states', 5)
        self.threshold = kwargs.pop('threshold', 4)
        self.random = kwargs.pop('random', True)
        if self.random:
            self.cur_state = np.random.choice(range(self.max_states))
        else:
            self.cur_state = kwargs.pop('init_state', 0)

    def neighbour_level(self) -> (int, int):
        return self.level, self.level

    def status(self) -> float:
        return self.cur_state

    def process(self, neighbours, cell_loc: (int, int)) -> float:
        """
        Rule:
        - a) Count how many neighbouring cells (Moore or Von Neumann neighborhoods) surround the cell with a
             value of the current cell’s state + 1
        - b) If the count is greater or equal to the threshold value then the cell state is incremented by 1

        :param neighbours:
        :param cell_loc:
        :return:
        """
        # neighbours[cell_loc[0]][cell_loc[1]] = 0
        check = (self.cur_state+1) % self.max_states
        mask = neighbours == check
        if mask.sum() >= self.threshold:
            self.cur_state = check

        return self.cur_state

    def reset(self) -> float:
        self.cur_state = 0.0
        return self.cur_state