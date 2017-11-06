import ast, getopt, sys

class SimplexSolver():

    def __init__(self):
        self.A = []
        self.b = []
        self.c = []

    def set_simplex_input(self, A, b, c):
        ''' Set initial variables here
        '''
        self.A = A
        self.b = b
        self.c = c

    def add_slack_variables(self):
        ''' Add slack variables to matrix A to transform
            inequalities to equalities.
        '''
        slack_vars = self._generate_identity(len(self.A))
        for i in range(0, len(slack_vars)):
            A[i] += slack_vars[i]
            A[i] += [b[i]]

    def create_tableau(self):
        self.add_slack_variables()
        A.append(c + [0] * (len(c)+1))

    def find_pivot(self):
        pass

    def _generate_identity(self, n):
        ''' Helper function for generating a square identity matrix.
        '''
        I = []
        for i in range(0, n):
            row = []
            for j in range(0, n):
                if i == j:
                    row.append(1)
                else:
                    row.append(0)
            I.append(row)
        return I

    def _str_matrix(self, M):
        ''' Generate string representation of some matrix M.
        '''
        str_mat = ""
        for row in M:
            str_mat += '| '
            if isinstance(row, list):
                for element in row:
                    str_mat += str(element) + ' '
            else:
                str_mat += str(row) + ' '
            str_mat += '|\n'                
        return str_mat

if __name__ == '__main__':
    print('\nSimplex Solver\n')

    ''' COMMAND LINE INPUT HANDLING '''
    A = []
    b = []
    c = []
    argv = sys.argv[1:]    
    try:
        opts, args = getopt.getopt(argv,"hA:b:c:",["A=","b=","c="])
    except getopt.GetoptError:
        print('simplex.py -A <matrix> -b <vector> -c <vector>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('simplex.py -A <matrix> -b <vector> -c <vector>')
            print('A: An mxn linear system. i.e. "[[1,0],[0,1]]"')
            print('b: Vector. Ax <= b')
            print('c: Vector. Coefficients of objective function.')
            sys.exit()
        elif opt in ("-A"):
            A = ast.literal_eval(arg)
        elif opt in ("-b"):
            b = ast.literal_eval(arg)
        elif opt in ("-c"):
            c = ast.literal_eval(arg)
    ''' END OF COMMAND LINE INPUT HANDLING '''

    ss = SimplexSolver()
    ss.set_simplex_input(A, b, c)

    print("1. Initial Matrix")
    print(ss._str_matrix(ss.A))

    ss.create_tableau()
    print("2. Create Simplex Tableau")
    print(ss._str_matrix(ss.A))
