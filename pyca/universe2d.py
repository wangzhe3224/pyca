from typing import List
import abc
from pyca.celltype import CellType
from numba import jit

import numpy as np


@jit(nopython=True)
def get_neighbours(snapshot: np.array, h_level, v_level, row, col) -> (np.array, (int, int)):
    """ get neighbours given h_level, v_level, and the location of the current cell in neighbours
    o is our target shell, return following slice of snapshot

    # TODO: Add a generic way to express neighbour pattern (Moore neighborhood). For example, x is target. But For now
    this can be handled by CellType.

    0 1 0
    1 x 1
    0 1 0

    Current it is always rectangular selection of neighbours:  von Neumann neighborhood

    x | x | x
    x | o | x
    x | x | x

    Corner cases:
    | o | x
    | x | x

    | x | x
    | o | x
    | x | x
    """
    row_l, col_l = snapshot.shape
    # fill neighbour
    res = snapshot[max(0, row - h_level): min(row_l, row + h_level + 1),
          max(0, col - v_level): min(col_l, col + v_level + 1)]

    # find row
    if row - h_level < 0:  # up row edge
        loc_r = max(row, row - h_level)
    else:  # normal cases
        loc_r = h_level

    # find col
    if col - v_level < 0:
        loc_c = max(col, col - v_level)
    else:
        loc_c = v_level

    return res, (loc_r, loc_c)


@jit(nopython=True)
def _process(cols, cur_status, new_status, rows, space):
    for row in range(rows):
        for col in range(cols):
            cell = space[row][col]  # type: CellType
            h_level, v_level = cell.neighbour_level()
            neighbours, (r, c) = get_neighbours(cur_status, h_level, v_level, row, col)
            state = cell.process(neighbours, (r, c))
            new_status[row][col] = state


class UniverseType(abc.ABC):
    """ A universe can do one thing: compute """

    @abc.abstractmethod
    def initialize(self, *args, **kwargs):
        """"""

    @abc.abstractmethod
    def register_cell_type(self, *arg, **kwargs):
        """"""

    @abc.abstractmethod
    def compute(self, *arg, **kwargs):
        """"""

    @abc.abstractmethod
    def __getitem__(self, item):
        """"""

    @abc.abstractmethod
    def __len__(self):
        """"""


class Universe2D(UniverseType):
    """"""

    def __init__(self, length: int, width: int):
        """"""
        self.length = length
        self.width = width
        # cell space to store cell type
        self._cell_space = np.empty((length, width), dtype=object)
        # time: list of grid
        # store cell representation
        self._steps = []  # type: List[np.array]
        self._initialized = False
        self._full_registered = False
        # Cache

    def initialize(self) -> np.array:
        """ """
        if not self._full_registered:
            raise ValueError('Universe is not fully filled by cells! Use register_cell_type')

        rows, cols = self.length, self.width
        _init_status = np.empty((rows, cols), dtype=np.float)
        for row in range(rows):  # Speed up this nest loops
            for col in range(cols):
                cell = self._cell_space[row][col]
                _init_status[row][col] = cell.status()

        self._steps.append(_init_status)
        self._initialized = True
        return _init_status

    def register_cell_type(self, cell: CellType, fill_strategy: str, **kwargs):
        """

        :param cell:
        :param fill_strategy: how to fill this cell?
        :return:
        """
        # TODO: full fill one type for now..
        rows, cols = self.length, self.width
        for row in range(rows):
            for col in range(cols):
                self._cell_space[row][col] = cell(**kwargs)

        self._full_registered = True

    def compute(self, step_limit=100):
        """ time passes """
        if not self._initialized or not self._full_registered:
            raise ValueError('Universe is not correctly initialized.')

        for time in range(1, step_limit+1):
            # print(time)
            snapshot = self._cell_space.copy()  # slow here.
            # evaluate
            _new_status = self.process(snapshot)
            # print(_new_status)
            self._steps.append(_new_status)

    def process(self, space) -> np.array:
        """ process one step

        return a new space
        """
        rows, cols = space.shape
        new_status = np.empty(space.shape)
        cur_status = self._steps[-1].copy()  # slow here

        _process(cols, cur_status, new_status, rows, space)

        return new_status

    @staticmethod
    @jit(nopython=True)
    def _process(cols, cur_status, new_status, rows, space):
        for row in range(rows):
            for col in range(cols):
                cell = space[row][col]  # type: CellType
                h_level, v_level = cell.neighbour_level()
                neighbours, (r, c) = get_neighbours(cur_status, h_level, v_level, row, col)
                state = cell.process(neighbours, (r, c))
                new_status[row][col] = state

    @staticmethod
    def get_neighbours(snapshot: np.array, h_level, v_level, row, col) -> (np.array, (int, int)):
        """ get neighbours given h_level, v_level, and the location of the current cell in neighbours
        o is our target shell, return following slice of snapshot

        # TODO: Add a generic way to express neighbour pattern (Moore neighborhood). For example, x is target. But For now
        this can be handled by CellType.

        0 1 0
        1 x 1
        0 1 0

        Current it is always rectangular selection of neighbours:  von Neumann neighborhood

        x | x | x
        x | o | x
        x | x | x

        Corner cases:
        | o | x
        | x | x

        | x | x
        | o | x
        | x | x
        """
        row_l, col_l = snapshot.shape
        # fill neighbour
        res = snapshot[max(0, row-h_level): min(row_l, row+h_level+1), max(0, col-v_level): min(col_l, col+v_level+1)]

        # find row
        if row - h_level < 0:  # up row edge
            loc_r = max(row, row-h_level)
        else:  # normal cases
            loc_r = h_level

        # find col
        if col - v_level < 0:
            loc_c = max(col, col-v_level)
        else:
            loc_c = v_level

        return res, (loc_r, loc_c)

    def __getitem__(self, item: int):
        return self._steps[item]

    def __len__(self):
        return len(self._steps)