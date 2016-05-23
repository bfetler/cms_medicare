import unittest
import pandas as pd
from cms_explore import getn

class CmsExploreTest(unittest.TestCase):

    def test_getn_numeric(self):
        "test generator numeric"
        ar = list(range(8))
        gx = getn(ar, 2)
        self.assertEqual(next(gx), [0, 1])
        self.assertEqual(next(gx), [2, 3])
        self.assertEqual(next(gx), [4, 5])
        self.assertEqual(next(gx), [6, 7])
        self.assertRaises(StopIteration, next, gx)

    def test_getn_alpha(self):
        "test generator alphabetical"
        ar = ['a','b','c','d','e','f']
        gx = getn(ar, 2)
        self.assertEqual(next(gx), ['a', 'b'])
        self.assertEqual(next(gx), ['c', 'd'])
        self.assertEqual(next(gx), ['e', 'f'])
        self.assertRaises(StopIteration, next, gx)

    def test_getn_alpha_odd(self):
        "test generator alphabetical w/ remainder array"
        ar = ['a','b','c','d','e','f']
        gx = getn(ar, 4)
        self.assertEqual(next(gx), ['a', 'b', 'c', 'd'])
        self.assertEqual(next(gx), ['e', 'f'])
        self.assertRaises(StopIteration, next, gx)

if __name__ == '__main__':
    unittest.main()

