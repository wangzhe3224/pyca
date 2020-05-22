from pyca.celltype import CellType


class BaseRule(CellType):
    """ DO not use this directly. Inherit this and specified rules. Check Rule30 for example """
    rules = {
    }

    def __init__(self, level=1, state=0):
        """"""
        self.level = level
        self.state = state

    def neighbour_level(self) -> (int, int):
        """"""
        return self.level, None

    def status(self) -> float:
        return self.state

    def process(self, neighbours, cell_loc: (int, int)) -> float:
        """ Rule 30: has 8 rules

        :param neighbours:
        :param cell_loc:
        :return:
        """
        try:
            return self.rules[tuple(neighbours.astype(int))]
        except KeyError:
            return 0.


class ClassicRule(BaseRule):
    """
    rule = ClassicRule('0110110')  # Rule100

    Follow the standard way of express 1D rule:
    https://en.wikipedia.org/wiki/Rule_110
    """

    def __init__(self, rule: str, level=1, state=0, **kwargs):
        """

        :param rule: 8 digit str, i.e. 0110110
        :param level:
        :param state:
        """
        super(ClassicRule, self).__init__(level=level, state=state)
        self.rule = rule
        _rules = [int(i) for i in rule]
        self.rules = {
            # 0 rules
            (1, 1, 1): _rules[0],
            (1, 1, 0): _rules[1],
            (1, 0, 1): _rules[2],
            (1, 0, 0): _rules[3],
            (0, 1, 1): _rules[4],
            (0, 1, 0): _rules[5],
            (0, 0, 1): _rules[6],
            (0, 0, 0): _rules[7],
            # conner case
            (1, 1): _rules[0],
            (1, 0): _rules[1],
            (0, 1): _rules[2],
            (0, 0): _rules[3],
        }

    def __str__(self):
        return 'Classic Rule: {}'.format(self.rule)

    def __repr__(self):
        return 'Classic Rule: {}'.format(self.rule)
