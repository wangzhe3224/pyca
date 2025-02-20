import numpy as np
from typing import List

from pyca.universe2d import UniverseType
from pyca.celltype import CellType
from pyca.switch import SwitchBase


class Universe1D(UniverseType):
    """"""
    def __init__(self, size: int, apply_different_rule=False, **kwargs):
        """ A 1D universe

        :param size: the size of 1d universe, length
        :param apply_different_rule: True means apply different rules for different step,
            if true, we need to pass in a Switch class to control logic of switching rules. Check ./example/switch_rules.py
            for details
        :param kwargs:
            if apply_different_rule, then must inject Switch object by switch key word.
        """
        self.size = size
        self._cell_space = np.empty((size, ), dtype=object)  # 1d array
        self._steps = []  # type: List[np.array]
        self._initialized = False
        self._full_registered = False
        self._apply_different_rule = apply_different_rule
        self._switch = None
        if apply_different_rule:
            switch = kwargs.pop('switch', None)  # type: SwitchBase
            if switch is None:
                raise ValueError('rule_list must be provided if apply_different_rule is True')
            self._switch = switch

    def initialize(self, *args, **kwargs):
        """ initialize universe """
        if not self._full_registered:
            raise ValueError('Universe is not fully filled by cells! Use register_cell_type')

        _init_status = np.empty((self.size, ), dtype=float)
        for item in range(self.size):
            cell = self._cell_space[item]  # type: CellType
            _init_status[item] = cell.status()

        self._steps.append(_init_status)
        self._initialized = True
        return _init_status

    def register_cell_type(self, cell: CellType, fill_strategy: str, **kwargs):
        """ Register cell type to universe with different fill strategy

        :param cell:
        :param fill_strategy: fill strategy for cells
            fill_pattern:
                - (Required) fill_pattern: list of states
            random:
                - (Optional) prob: probability for 1 state, default 0.5
            single:
                - (Optional) pos: position in the init
        :param kwargs: parameters for different fill strategy
        :return:
        """
        if fill_strategy == 'fill_pattern':
            pattern = kwargs.get(fill_strategy)
            if len(pattern) != self.size:
                raise ValueError('Pattern size does not match universe size!')
            for idx, i in enumerate(pattern):
                self._cell_space[idx] = cell(state=i, **kwargs)
        elif fill_strategy == 'random':
            prob = kwargs.pop('prob', 0.5)
            for i in range(self.size):
                state = np.random.choice([0, 1], p=[1-prob, prob])
                self._cell_space[i] = cell(state=state, **kwargs)
        elif fill_strategy == 'single':
            loc = kwargs.pop('pos', self.size//2)
            for i in range(self.size):
                if i == loc:
                    self._cell_space[i] = cell(state=1, **kwargs)
                else:
                    self._cell_space[i] = cell(state=0, **kwargs)
        else:
            for i in range(self.size):
                self._cell_space[i] = cell(**kwargs)

        self._full_registered = True

    def compute(self, step_limit):
        """ https://en.wikipedia.org/wiki/Cellular_automaton#/media/File:One-d-cellular-automate-rule-30.gif

        :param step_limit:
        :return:
        """
        if not self._initialized or not self._full_registered:
            raise ValueError('Universe is not correctly initialized.')

        for time in range(step_limit):
            if self._apply_different_rule:
                new_rule = self._switch.next()
                snapshot = np.empty((self.size, ), dtype=object)
                for i in range(self.size):
                    snapshot[i] = new_rule
                _new_status = self.process(snapshot)
                self._steps.append(_new_status)
            else:
                snapshot = self._cell_space.copy()
                _new_status = self.process(snapshot)
                self._steps.append(_new_status)

    def process(self, snapshot):
        """ process one step with current cell stats

        :param snapshot: a copy if current cell space
        :return:
        """
        new_status = np.empty(snapshot.shape)
        cur_status = self._steps[-1]
        for i in range(self.size):
            cell = snapshot[i]  # type: CellType
            level, _ = cell.neighbour_level()
            neighbours, loc = self.get_neighbours(cur_status, level, i)
            # print(cur_status, level, i, neighbours, loc)
            state = cell.process(neighbours, (loc, None))
            new_status[i] = state

        return new_status

    @staticmethod
    def get_neighbours(snapshot: np.array, level, loc) -> (np.array, int):
        """"""
        nei = snapshot[max(0, loc-level): min(loc+level+1, len(snapshot))]
        if loc - level < 0:
            res = max(loc, loc-level)
        else:
            res = level
        return nei, res

    def __getitem__(self, item):
        return self._steps[item]

    def __len__(self):
        return len(self._steps)

    def form_matrix(self):
        return np.stack(self._steps)

    def form_step_matrix(self):
        """"""
        shape = (len(self._steps), len(self._steps[0]))
        res = []
        _tmp = np.zeros(shape)
        for idx, step in enumerate(self._steps):
            _tmp[idx, :] = step
            res.append(_tmp.copy())

        return res