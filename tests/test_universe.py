import unittest

import numpy as np

from pyca.universe2d import Universe2D


class TestUniverse(unittest.TestCase):

    def setUp(self) -> None:
        self.universe = Universe2D(100, 100)

    def test_get_neighbours_slow(self):

        snap = np.array(range(25), dtype=np.float).reshape((5, 5))
        print(snap)

        # Corner cases
        n1, (r, c) = self.universe.get_neighbours(snap, 1, 1, 0, 0)
        assert np.array_equal(n1, np.array([0, 1, 5, 6]).reshape((2, 2)))
        assert r == 0
        assert c == 0

        n1, (r, c) = self.universe.get_neighbours(snap, 2, 2, 0, 0)
        assert np.array_equal(n1, np.array([0, 1, 2, 5, 6, 7, 10, 11, 12]).reshape((3, 3)))
        assert r == 0
        assert c == 0

        n, (r, c) = self.universe.get_neighbours(snap, 1, 1, 4, 4)
        # print(n, r, c)
        assert np.array_equal(n, np.array([18, 19, 23, 24]).reshape(2, 2))
        assert r == 1
        assert c == 1

        n, (r, c) = self.universe.get_neighbours(snap, 1, 1, 4, 0)
        # print(n, r, c)
        assert np.array_equal(n, np.array([15, 16, 20, 21]).reshape(2, 2))
        assert r == 1
        assert c == 0

        n, (r, c) = self.universe.get_neighbours(snap, 1, 1, 0, 4)
        # print(n, r, c)
        assert np.array_equal(n, np.array([3, 4, 8, 9]).reshape(2, 2))
        assert r == 0
        assert c == 1

        # Edge cases:
        n, (r, c) = self.universe.get_neighbours(snap, 1, 1, 0, 1)
        assert np.array_equal(n, np.array([0, 1, 2, 5, 6, 7]).reshape((2, 3)))
        assert r == 0
        assert c == 1

        n, (r, c) = self.universe.get_neighbours(snap, 1, 1, 4, 1)
        assert r == 1
        assert c == 1

        n, (r, c) = self.universe.get_neighbours(snap, 1, 1, 1, 0)
        assert r == 1
        assert c == 0

        # Normal cases:
        n, (r, c) = self.universe.get_neighbours(snap, 1, 1, 1, 1)
        assert np.array_equal(n, np.array([0, 1, 2, 5, 6, 7, 10, 11, 12]).reshape((3, 3)))
        assert r == 1
        assert c == 1

