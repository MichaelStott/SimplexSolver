import ast, getopt, sys, copy, os
from fractions import Fraction
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class SimplexSolver():
    ''' Solves linear programs that are in standard form.
    '''
    
    def __init__(self):
        self.A = []
        self.b = []
        self.c = []
        self.tableau = []

    def set_simplex_input(self, A, b, c):
        ''' Set initial variables and create tableau.
        '''
        for a in A:
            self.A.append([Fraction(x) for x in a])
        self.b = [Fraction(x) for x in b]
        self.c = [Fraction(x) for x in c]
        self.create_tableau()

    def add_slack_variables(self):
        ''' Add slack & artificial variables to matrix A to transform
            all inequalities to equalities.
        '''
        slack_vars = self._generate_identity(len(self.tableau))
        for i in range(0, len(slack_vars)):
            self.tableau[i] += slack_vars[i]
            self.tableau[i] += [self.b[i]]

    def create_tableau(self):
        ''' Create initial tableau table.
        '''
        self.tableau = copy.deepcopy(self.A)
        self.add_slack_variables()
        c = copy.deepcopy(self.c)
        for index, value in enumerate(c):
            c[index] = -value
        self.tableau.append(c + [0] * (len(c)+1))

    def find_pivot(self):
        ''' Find pivot index.
        '''
        enter_index = self.get_entering_var()
        depart_index = self.get_departing_var(enter_index)
        return [enter_index, depart_index]

    def pivot(self, pivot_index):
        ''' Perform operations on pivot.
        '''
        i, j = pivot_index

        pivot = self.tableau[i][j]
        self.tableau[i] = [element / pivot for
                           element in self.tableau[i]]
        for index, row in enumerate(self.tableau):
           if index != i:
              row_scale = [y * self.tableau[index][j]
                          for y in self.tableau[i]]
              self.tableau[index] = [x - y for x,y in
                                     zip(self.tableau[index],
                                         row_scale)]
        
    def get_entering_var(self):
        ''' Get entering variable by determining the 'most negative'
            element.
        '''
        bottom_row = self.tableau[len(self.tableau) - 1]
        print("BOTTOM ROW: %s" % str(bottom_row))
        most_neg_ind = 0
        most_neg = bottom_row[most_neg_ind]
        for index, value in enumerate(bottom_row):
            if value < most_neg:
                most_neg = value
                most_neg_ind = index
        return most_neg_ind
            

    def get_departing_var(self, entering_index):
        ''' To calculate the departing variable, get them minimum of the ratio
            of b (b_i) to the corresponding value in the entering collumn. 
        '''
        skip = 0
        min_ratio_index = 0
        min_ratio = -1
        for index, x in enumerate(self.tableau):
            if x[entering_index] > 0:
                skip = index
                min_ratio_index = index
                min_ratio = x[len(x)-1]/x[entering_index]
                break
        
        if min_ratio > 0:
            for index, x in enumerate(self.tableau):
                if index > skip and x[entering_index] > 0:
                    ratio = x[len(x)-1]/x[entering_index]
                    if min_ratio > ratio:
                        min_ratio = ratio
                        min_ratio_index = index
        
        return min_ratio_index
            

    def get_Ab(self):
        ''' Get A matrix with b vector appended.
        '''
        matrix = copy.deepcopy(self.A)
        for i in range(0, len(matrix)):
            matrix[i] += [self.b[i]]
        return matrix

    def should_terminate(self):
        ''' Determines whether there are any negative elements
            on the bottom row
        '''
        result = True
        index = len(ss.tableau) - 1
        for i, x in enumerate(ss.tableau[index]):
            if x < 0 and i != len(ss.tableau[index]) - 1:
                result = False
        return result
    
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
        for row in M:
            for val in row:
                print '{:6}'.format(val),
            print

if __name__ == '__main__':
    clear()
    
    def prompt():
        raw_input("Press enter to continue...")

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
    if not A or not b or not c:
        print('Must provide arguments for A, b, c (use -h for more info)')
        sys.exit()
    ''' END OF COMMAND LINE INPUT HANDLING '''

    ss = SimplexSolver()
    ss.set_simplex_input(A, b, c)

    # Add slack & artificial variables
    print("Create initial tableau.")
    ss._str_matrix(ss.tableau)
    prompt()

    # Are there any negative elements on the bottom (disregarding right-most
    # element...)
    while (not ss.should_terminate()):
        # ... if so, continue.
        print("\nThere are negative elements in the bottom row. "
              "Therefore, the algorithm will continue.\n")

        # Get the pivot element.
        print("\nFind pivot for this iteration.")
        pivot = ss.find_pivot()

        if ss.tableau[pivot[0]][pivot[1]] == 0:
            print ("Zero pivot detected.")
            print ("Solution is infeasible.")
            sys.exit(0)
        
        print("Pivot: %s" % str(pivot))
        prompt()

        # Do row operations to make every other element in column zero.
        print("\nDo row operations.")
        ss.pivot(pivot)
        ss._str_matrix(ss.tableau)
        prompt()
        # For readability, clear the current console output.
        clear()
    print("That's all folks!")
