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

            Source: http://mat.gsia.cmu.edu/classes/QUANT/NOTES/chap7.pdf, Example 7.2.1
        '''
        self.assertDictEqual({'x_1': Fraction(5,3),
                              'x_2': Fraction(2,3),
                              's_1': Fraction(0),
                              's_2': Fraction(0),
                              'z': Fraction(7,3)},
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

            Source: http://college.cengage.com/mathematics/larson/elementary_linear/4e/shared/downloads/c09s3.pdf, Example 1
        '''
        self.assertDictEqual({'x_1': Fraction(15),
                              'x_2': Fraction(12),
                              's_1': Fraction(14),
                              's_2': Fraction(0),
                              's_3': Fraction(0),
                              'z': Fraction(132)},
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

            Source: http://college.cengage.com/mathematics/larson/elementary_linear/4e/shared/downloads/c09s3.pdf, Example 2
        '''
        self.assertDictEqual({'x_1': Fraction(5),
                              'x_2': Fraction(0),
                              'x_3': Fraction(5,2),
                              's_1': Fraction(0),
                              's_2': Fraction(20),
                              's_3': Fraction(0),
                              'z': Fraction(15)},
                              SimplexSolver().run_simplex([[2,1,0],
                                                           [1,2,-2],
                                                           [0,1,2]],
                                                          [10,20,5],
                                                          [2,-1,2]))

    def test_max_feasible4(self):
        ''' Find optimal solution to max(2x1 - x2 + 2x3) such that:
            Ax <= b,
            x1, x2, x3 >= 0,
            A =  |4 1 1|, b = |30|, c = |3|
                 |2 3 1|      |60|      |2|
                 |1 2 3|      |40|      |1|

            Source: http://college.cengage.com/mathematics/larson/elementary_linear/4e/shared/downloads/c09s3.pdf, Example 3
        '''
        self.assertDictEqual({'x_1': Fraction(3),
                              'x_2': Fraction(18),
                              'x_3': Fraction(0),
                              's_1': Fraction(0),
                              's_2': Fraction(0),
                              's_3': Fraction(1),
                              'z': Fraction(45)},
                              SimplexSolver().run_simplex([[4,1,1],
                                                           [2,3,1],
                                                           [1,2,3]],
                                                          [30,60,40],
                                                          [3,2,1]))

    def test_max_feasible5(self):
        ''' Find optimal solution to max(11x1 + 16x2 + 15x3) such that:
            Ax <= b,
            x1, x2, x3 >= 0,
            A =  | 1   2  3/2|, b = |12000|, c = |11|
                 |2/3 2/3  1 |      | 4600|      |16|
                 |1/2 1/3 1/2|      | 2400|      |15|

            Source: http://college.cengage.com/mathematics/larson/elementary_linear/4e/shared/downloads/c09s3.pdf, Example 4
        '''
        self.assertDictEqual({'x_1': Fraction(600),
                              'x_2': Fraction(5100),
                              'x_3': Fraction(800),
                              's_1': Fraction(0),
                              's_2': Fraction(0),
                              's_3': Fraction(0),
                              'z': Fraction(100200)},
                              SimplexSolver().run_simplex([[1,2,Fraction(3,2)],
                                                           [Fraction(2,3),
                                                            Fraction(2,3),1],
                                                           [Fraction(1,2),
                                                            Fraction(1,3),
                                                            Fraction(1,2)]],
                                                          [12000,4600,2400],
                                                          [11,16,15]))

    def test_max_feasible6(self):
        ''' Find optimal solution to max(11x1 + 16x2 + 15x3) such that:
            Ax <= b,
            x1, x2, x3 >= 0,
            A =  |20  6  3|, b = |182|, c = |100000|
                 | 0  1  0|      | 10|      | 40000|
                 |-1 -1  1|      |  0|      | 18000|
                 |-9  1  1|      |  0|

            Source: http://college.cengage.com/mathematics/larson/elementary_linear/4e/shared/downloads/c09s3.pdf, Example 5
        '''
        self.assertDictEqual({'x_1': Fraction(4),
                              'x_2': Fraction(10),
                              'x_3': Fraction(14),
                              's_1': Fraction(0),
                              's_2': Fraction(0),
                              's_3': Fraction(0),
                              's_4': Fraction(12),
                              'z': Fraction(1052000)},
                              SimplexSolver().run_simplex([[20,6,3],
                                                           [0,1,0],
                                                           [-1,-1,1],
                                                           [-9,1,1]],
                                                          [182,10,0,0],
                                                          [100000,
                                                           40000,
                                                           18000]))
    ''' STANDARD FORM MINIMIZATION PROBLEMS '''
    def test_min_feasible1(self):
        ''' Find optimal solution to min(3x1 + 2x2) such that:         
            Ax >= b,
            x1, x2 >= 0,
            A = |2, 1|, b = |6|, c = |3|
                |1, 1|      |4|      |2|

            Source: http://college.cengage.com/mathematics/larson/elementary_linear/4e/shared/downloads/c09s4.pdf, Example 1
        '''
        self.assertDictEqual({'x_1': Fraction(2),
                              'x_2': Fraction(2),
                              's_1': Fraction(0),
                              's_2': Fraction(0),
                              'y_1': Fraction(1),
                              'y_2': Fraction(1),
                              'z': Fraction(10)},
                              SimplexSolver().run_simplex([[2,1],
                                                           [1,1]],
                                                          [6,4],
                                                          [3,2],
                                                          prob='min'))

    def test_min_feasible2(self):
        ''' Find optimal solution to min(2x1 + 10x2 + 8x3) such that:
            Ax >= b,
            x1, x2, x3 >= 0,
            A = | 1 1 1|, b = |6|, c = | 2|
                | 0 1 2|      |8|      |10|
                |-1 2 2|      |4|      | 8|

            Source: http://college.cengage.com/mathematics/larson/elementary_linear/4e/shared/downloads/c09s4.pdf, Example 2
        '''
        self.assertDictEqual({'x_1': Fraction(2),
                              'x_2': Fraction(0),
                              'x_3': Fraction(4),
                              's_1': Fraction(0),
                              's_2': Fraction(5),
                              's_3': Fraction(0),
                              'y_1': Fraction(2),
                              'y_2': Fraction(3),
                              'y_3': Fraction(0),
                              'z': Fraction(36)},
                              SimplexSolver().run_simplex([[1,1,1],
                                                           [0,1,2],
                                                           [-1,2,2]],
                                                          [6,8,4],
                                                          [2,10,8],
                                                          prob='min'))

    def test_min_feasible3(self):
        ''' Find optimal solution to min(20000x1 + 25000x2) such that:
            Ax >= b,
            x1, x2 >= 0,
            A = |400 300|, b = |25000|, c = |20000|
                |300 400|      |27000|      |25000|
                |200 500|      |30000|

            Source: http://college.cengage.com/mathematics/larson/elementary_linear/4e/shared/downloads/c09s4.pdf, Example 3
        '''
        self.assertDictEqual({'x_1': Fraction(25),
                              'x_2': Fraction(50),
                              's_1': Fraction(0),
                              's_2': Fraction(0),
                              'y_1': Fraction(250,7),
                              'y_2': Fraction(0),
                              'y_3': Fraction(200, 7),
                              'z': Fraction(1750000)},
                              SimplexSolver().run_simplex([[400,300],
                                                           [300,400],
                                                           [200,500]],
                                                          [25000,
                                                           27000,
                                                           30000],
                                                          [20000,25000],
                                                          prob='min'))
if __name__ == '__main__':
    unittest.main()
