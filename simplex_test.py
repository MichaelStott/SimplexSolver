from simplex import SimplexSolver
from fractions import Fraction
import unittest


class SimplexSolverTest(unittest.TestCase):

    ''' STANDARD FORM MAXIMIZATION EXAMPLES '''
    def test_max_feasible1(self):
        ''' Find optimal solution to max(x1 + x2) such that:
            Ax <= b,
            x1, x2 >= 0,
            A =  |2 1|, b = |4|, c = |1|
                 |1 2|      |3|      |1|

            Source: http://mat.gsia.cmu.edu/classes/QUANT/NOTES/chap7.pdf
                    Example 7.2.1
        '''
        self.assertDictEqual({'x0': Fraction(5,3),
                              'x1': Fraction(2,3),
                              's0': Fraction(0),
                              's1': Fraction(0),
                              'opt': Fraction(7,3)},
                              SimplexSolver().run_simplex([[2,1],
                                                           [1,2]],
                                                          [4,3],
                                                          [1,1]))

    def test_max_feasible2(self):
        ''' Find optimal solution to max(4x1 + 6x2) such that:
            Ax <= b,
            x1, x2 >= 0,
            A =  |-1 1|, b = |11|, c = |4|
                 | 1 1|      |27|      |6|
                 | 2 5|      |90|

            Source: http://college.cengage.com/mathematics/larson/elementary_linear/4e/shared/downloads/c09s3.pdf
                    Example 1
        '''
        self.assertDictEqual({'x0': Fraction(15),
                              'x1': Fraction(12),
                              's0': Fraction(14),
                              's1': Fraction(0),
                              's2': Fraction(0),
                              'opt': Fraction(132)},
                              SimplexSolver().run_simplex([[-1,1],
                                                           [1,1],
                                                           [2,5]],
                                                          [11,27,90],
                                                          [4,6]))

    def test_max_feasible3(self):
        ''' Find optimal solution to max(2x1 - x2 + 2x3) such that:
            Ax <= b,
            x1, x2 >= 0,
            A =  |2 1  0|, b = |10|, c = | 2|
                 |1 2 -2|      |20|      |-1|
                 |0 1  2|      | 5|      | 2|

            Source: http://college.cengage.com/mathematics/larson/elementary_linear/4e/shared/downloads/c09s3.pdf
                    Example 2
        '''
        self.assertDictEqual({'x0': Fraction(5),
                              'x1': Fraction(0),
                              'x2': Fraction(5,2),
                              's0': Fraction(0),
                              's1': Fraction(20),
                              's2': Fraction(0),
                              'opt': Fraction(15)},
                              SimplexSolver().run_simplex([[2,1,0],
                                                           [1,2,-2],
                                                           [0,1,2]],
                                                          [10,20,5],
                                                          [2,-1,2])

if __name__ == '__main__':
    unittest.main()
