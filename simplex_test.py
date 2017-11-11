from simplex import SimplexSolver
from fractions import Fraction
import unittest

class SimplexSolverTest(unittest.TestCase):

    def test_2x2_feasible1(self):
        self.assertDictEqual({'x0': Fraction(5,3),
                              'x1': Fraction(2,3),
                              's0': Fraction(0),
                              's1': Fraction(0),
                              'opt': Fraction(7,3)},
                              SimplexSolver().run_simplex([[2,1],[1,2]],
                                                          [4,3], [1,1]))

if __name__ == '__main__':
    unittest.main()
