import numpy as np

from pyca.celltype import CellType
from pyca.rules.BaseRule import ClassicRule
from typing import List


class SwitchBase(object):

    def next(self, **kwargs) -> CellType:
        """ get next cell vector """


class ClassicSwitch1D(SwitchBase):

    def __init__(self, rule_list: List[str], window=10):
        """ switch rule every window times """
        self.rule_list = rule_list
        self.rules = []  # type: List[CellType]
        for item in rule_list:
            cell = ClassicRule(rule=item)
            self.rules.append(cell)
        self._counter = 1
        self._rule_counter = 0
        self.window = window
        self.current_rule = self.rules[0]

    def next(self, **kwargs) -> ClassicRule:
        """"""
        if self._counter % self.window == 0:
            idx = self._rule_counter % len(self.rule_list)
            rule = self.rules[idx]
            self._rule_counter += 1
            self._counter += 1
            self.current_rule = rule
            return rule
        else:
            self._counter += 1
            return self.current_rule

