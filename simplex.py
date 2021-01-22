import ast, getopt, sys, copy, os
from fractions import Fraction

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')


class SimplexSolver():
    ''' Solves linear programs using simplex algorithm and
        output problem steps in LaTeX file.
    '''

    # Table for converting inequality list to LaTeX    
    latex_ineq = {'=': '=',
                  '<=': r'\leq',
                  '>=': r'\geq'}

    def __init__(self):
        self.A = []
        self.b = []
        self.c = []
        self.tableau = []
        self.entering = []
        self.departing = []
        self.ineq = []
        self.prob = "max"
        self.gen_doc = False
        self.doc = ""

    def run_simplex(self, A, b, c, prob='max', ineq=[],
                    enable_msg=False, latex=False):
        ''' Run simplex algorithm.
        '''
        self.prob = prob
        self.gen_doc = latex
        self.ineq = ineq

        # Create the header for the latex doc.        
        self.start_doc()

        # Add slack & artificial variables
        self.set_simplex_input(A, b, c)
            
        # Are there any negative elements on the bottom (disregarding
        # right-most element...)
        while (not self.should_terminate()):
            # ... if so, continue.
            if(enable_msg):
                clear()
                self._print_tableau()
                print(("Current solution: %s\n" %
                      str(self.get_current_solution())))
                self._prompt()
            
            # Attempt to find a non-negative pivot.
            pivot = self.find_pivot()
            if pivot[1] < 0:
                if (enable_msg):
                    print ("There exists no non-negative pivot. "
                           "Thus, the solution is infeasible.")
                self.infeasible_doc()
                self.print_doc()
                return None
            else:
                self.pivot_doc(pivot)
                if (enable_msg):
                    clear()
                    self._print_tableau()
                    print(("\nThere are negative elements in the bottom row, "
                          "so the current solution is not optimal. "
                          "Thus, pivot to improve the current solution. The "
                          "entering variable is %s and the departing "
                          "variable is %s.\n" %
                           (str(self.entering[pivot[0]]),
                           str(self.departing[pivot[1]]))))
                    self._prompt()
                    print("\nPerform elementary row operations until the "
                          "pivot is one and all other elements in the "
                          "entering column are zero.\n")

            # Do row operations to make every other element in column zero.
            self.pivot(pivot)
            self.tableau_doc()

        solution = self.get_current_solution()
        self.final_solution_doc(solution)
        if (enable_msg):
            clear()
            self._print_tableau()
            print(("Current solution: %s\n" % str(solution)))
            print("That's all folks!")
        self.print_doc()
        return solution
        
    def set_simplex_input(self, A, b, c):
        ''' Set initial variables and create tableau.
        '''
        # Convert all entries to fractions for readability.
        for a in A:
            self.A.append([Fraction(x) for x in a])    
        self.b = [Fraction(x) for x in b]
        self.c = [Fraction(x) for x in c]
        if not self.ineq:
            if self.prob == 'max':
                self.ineq = ['<='] * len(b)
            elif self.prob == 'min':
                self.ineq = ['>='] * len(b)
            
        self.update_enter_depart(self.get_Ab())
        self.init_problem_doc()

        # If this is a minimization problem...
        if self.prob == 'min':
            # ... find the dual maximum and solve that.
            m = self.get_Ab()
            m.append(self.c + [0])
            m = [list(t) for t in zip(*m)] # Calculates the transpose
            self.A = [x[:(len(x)-1)] for x in m]
            self.b = [y[len(y) - 1] for y in m]
            self.c = m[len(m) -1]
            self.A.pop()
            self.b.pop()
            self.c.pop()
            self.ineq = ['<='] * len(self.b)

        self.create_tableau()
        self.ineq = ['='] * len(self.b)
        self.update_enter_depart(self.tableau)
        self.slack_doc()
        self.init_tableau_doc()

    def update_enter_depart(self, matrix):
        self.entering = []
        self.departing = []
        # Create tables for entering and departing variables
        for i in range(0, len(matrix[0])):
            if i < len(self.A[0]):
                prefix = 'x' if self.prob == 'max' else 'y'
                self.entering.append("%s_%s" % (prefix, str(i + 1)))
            elif i < len(matrix[0]) - 1:
                self.entering.append("s_%s" % str(i + 1 - len(self.A[0])))
                self.departing.append("s_%s" % str(i + 1 - len(self.A[0])))
            else:
                self.entering.append("b")

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
        self.tableau.append(c + [0] * (len(self.b)+1))

    def find_pivot(self):
        ''' Find pivot index.
        '''
        enter_index = self.get_entering_var()
        depart_index = self.get_departing_var(enter_index)
        return [enter_index, depart_index]

    def pivot(self, pivot_index):
        ''' Perform operations on pivot.
        '''
        j,i = pivot_index

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

        self.departing[i] = self.entering[j]
        
    def get_entering_var(self):
        ''' Get entering variable by determining the 'most negative'
            element of the bottom row.
        '''
        bottom_row = self.tableau[len(self.tableau) - 1]
        most_neg_ind = 0
        most_neg = bottom_row[most_neg_ind]
        for index, value in enumerate(bottom_row):
            if value < most_neg:
                most_neg = value
                most_neg_ind = index
        return most_neg_ind
            

    def get_departing_var(self, entering_index):
        ''' To calculate the departing variable, get the minimum of the ratio
            of b (b_i) to the corresponding value in the entering collumn. 
        '''
        skip = 0
        min_ratio_index = -1
        min_ratio = 0
        for index, x in enumerate(self.tableau):
            if x[entering_index] != 0 and x[len(x)-1]/x[entering_index] > 0:
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
        index = len(self.tableau) - 1
        for i, x in enumerate(self.tableau[index]):
            if x < 0 and i != len(self.tableau[index]) - 1:
                result = False
        return result

    def get_current_solution(self):
        ''' Get the current solution from tableau.
        '''
        solution = {}
        for x in self.entering:
            if x is not 'b':
                if x in self.departing:
                    solution[x] = self.tableau[self.departing.index(x)]\
                                  [len(self.tableau[self.departing.index(x)])-1]
                else:
                    solution[x] = 0
        solution['z'] = self.tableau[len(self.tableau) - 1]\
                          [len(self.tableau[0]) - 1]
        
        # If this is a minimization problem...
        if (self.prob == 'min'):
            # ... then get x_1, ..., x_n  from last element of
            # the slack columns.
            bottom_row = self.tableau[len(self.tableau) - 1]
            for v in self.entering:
                if 's' in v:
                    solution[v.replace('s', 'x')] = bottom_row[self.entering.index(v)]    

        return solution

    def start_doc(self):
        if not self.gen_doc:
            return
        self.doc = (r"\documentclass{article}"
                    r"\usepackage{amsmath}"
                    r"\begin{document}"
                    r"\title{Simplex Solver}"
                    r"\maketitle"
                    r"\begin{flushleft}"
                    r"\textbf{Problem}"
                    r"\end{flushleft}")

    def init_problem_doc(self):
        if not self.gen_doc:
            return
        # Objective function.
        self.doc += (r"\begin{flushleft}"
                     r"Given the following linear system and objective "
                     r"function, find the optimal solution."
                     r"\end{flushleft}"
                     r"\begin{equation*}")
        func = ""
        found_value = False
        for index, x in enumerate(self.c):
            opp = '+'
            if x == 0:
                continue
            if x < 0:
                opp = ' - '
            elif index == 0 or not found_value:
                opp = ''
            if x == 1 or x == -1:
                x = ''
            func += (r"%s %sx_%s "  % (opp, str(x), str(index+1)))
            found_value = True
        self.doc += (r"\max{%s} \\ "
                     r"\end{equation*}" % func)
        self.linear_system_doc(self.get_Ab())
        self.doc += (r"\begin{flushleft}"
                     r"\textbf{Solution}"
                     r"\end{flushleft}")

    def linear_system_doc(self, matrix):
        if not self.gen_doc:
            return
        self.doc += (r"\["
                     r"\left\{"
                     r"\begin{array}{c}")
        for i in range(0, len(matrix)):
            found_value = False
            for index, x in enumerate(matrix[i]):
                opp = '+'
                if x == 0 and index != len(matrix[i]) - 1:
                    continue
                if x < 0:
                    opp = '-'
                elif index == 0 or not found_value:
                    opp = ''
                if index != len(matrix[i]) - 1:
                    if x == 1 or x == -1:
                        x = ''
                    self.doc += (r"%s %s%s "  % (opp, str(x),
                                                 str(self.entering[index])))
                else:
                    self.doc += (r"%s %s"  % (self.latex_ineq[self.ineq[i]],str(x)))
                found_value = True
                if (index == len(matrix[i]) - 1):
                    self.doc += r" \\ "        
        self.doc += (r"\end{array}"
                     r"\right."
                     r"\]")
 
    def slack_doc(self):
        if not self.gen_doc:
            return
        self.doc += (r"\begin{flushleft}"
                     r"Add slack variables to turn "
                     r"all inequalities to equalities."
                     r"\end{flushleft}")
        self.linear_system_doc(self.tableau[:len(self.tableau)-1])

    def init_tableau_doc(self):
        if not self.gen_doc:
            return
        self.doc += (r"\begin{flushleft}"
                     r"Create the initial tableau of the new linear system."
                     r"\end{flushleft}")
        self.tableau_doc()
            
    def tableau_doc(self):
        if not self.gen_doc:
            return
        self.doc += r"\begin{equation*}"
        self.doc += r"\begin{bmatrix}"
        self.doc += r"\begin{array}{%s|c}" % ("c" * (len(self.tableau[0])-1))
        for index, var in enumerate(self.entering):
            if index != len(self.entering) - 1:
                self.doc += r"%s &" % var
            else:
                self.doc += r"%s \\ \hline" % var
        for indexr, row in enumerate(self.tableau):
            for indexv, value in enumerate(row):
                if indexv != (len(row)-1):
                    self.doc += r"%s & " % (str(value))
                elif indexr != (len(self.tableau)-2):
                    self.doc += r"%s \\" % (str(value))
                else:
                    self.doc += r"%s \\ \hline" % (str(value))
        self.doc += r"\end{array}"
        self.doc += r"\end{bmatrix}"
        self.doc += (r"\begin{array}{c}"
                     r"\\")
        for var in self.departing:
            self.doc += (r"%s \\" % var)
        self.doc += r"\\"
        self.doc += r"\end{array}"
        self.doc += r"\end{equation*}"

    def infeasible_doc(self):
        if not self.gen_doc:
            return
        self.doc += (r"\begin{flushleft}"
                     r"There are no non-negative candidates for the pivot. "
                     r"Thus, the solution is infeasible."
                     r"\end{flushleft}")

    def pivot_doc(self, pivot):
        if not self.gen_doc:
            return
        self.doc += (r"\begin{flushleft}"
                     r"There are negative elements in the bottom row, "
                     r"so the current solution is not optimal. "
                     r"Thus, pivot to improve the current solution. The "
                     r"entering variable is $%s$ and the departing "
                     r"variable is $%s$."
                     r"\end{flushleft}" %
                     (str(self.entering[pivot[0]]),
                     str(self.departing[pivot[1]])))
        self.doc += (r"\begin{flushleft}"
                     r"Perform elementary row operations until the "
                     r"pivot element is 1 and all other elements in the "
                     r"entering column are 0."
                     r"\end{flushleft}")
    
    def current_solution_doc(self, solution):
        if not self.gen_doc:
            return
        self.doc += r"\begin{equation*}"
        for key,value in sorted(solution.items()):
            self.doc += r"%s = %s" % (key, self._fraction_to_latex(value))
            if key != 'z':
                self.doc += r", "
        self.doc += r"\end{equation*}"

    def final_solution_doc(self, solution):
        if not self.gen_doc:
            return
        self.doc += (r"\begin{flushleft}"
                     r"There are no negative elements in the bottom row, so "
                     r"we know the solution is optimal. Thus, the solution is: "
                     r"\end{flushleft}")
        self.current_solution_doc(solution)

    def print_doc(self):
        if not self.gen_doc:
            return
        self.doc += (r"\end{document}")
        with open("solution.tex", "w") as tex:
            tex.write(self.doc)

    def _fraction_to_latex(self, fract):
        if fract.denominator == 1:
            return str(fract.numerator)
        else:
            return r"\frac{%s}{%s}" % (str(fract.numerator), str(fract.denominator))

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
        
    def _print_matrix(self, M):
        ''' Print some matrix.
        '''
        for row in M:
            print('|', end=' ')
            for val in row:
                print('{:^5}'.format(str(val)), end=' ')
            print('|')

    def _print_tableau(self):
        ''' Print simplex tableau.
        '''
        print(' ', end=' ')
        for val in self.entering:
            print('{:^5}'.format(str(val)), end=' ')
        print(' ')
        for num, row in enumerate(self.tableau):
            print('|', end=' ')
            for index, val in enumerate(row):
                print('{:^5}'.format(str(val)), end=' ')
            if num < (len(self.tableau) -1):
                print('| %s' % self.departing[num])
            else:
                print('|')

    def _prompt(self):
        input("Press enter to continue...")

if __name__ == '__main__':
    clear()

    ''' COMMAND LINE INPUT HANDLING '''
    A = []
    b = []
    c = []
    p = ''
    argv = sys.argv[1:]    
    try:
        opts, args = getopt.getopt(argv,"hA:b:c:p:",["A=","b=","c=","p="])
    except getopt.GetoptError:
        print('simplex.py -A <matrix> -b <vector> -c <vector> -p <type>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('simplex.py -A <matrix> -b <vector> -c <vector> -p <obj_func_type>')
            print('A: Matrix that represents coefficients of constraints.')
            print('b: Ax <= b')
            print('c: Coefficients of objective function.')
            print('p: Indicates max or min objective function.')
            sys.exit()
        elif opt in ("-A"):
            A = ast.literal_eval(arg)
        elif opt in ("-b"):
            b = ast.literal_eval(arg)
        elif opt in ("-c"):
            c = ast.literal_eval(arg)
        elif opt in ("-p"):
            p = arg.strip()
    if not A or not b or not c:
        print('Must provide arguments for A, b, c (use -h for more info)')
        sys.exit()
    ''' END OF COMMAND LINE INPUT HANDLING '''

    # Assume maximization problem as default.
    if p not in ('max', 'min'):
        p = 'max'
    
    SimplexSolver().run_simplex(A,b,c,prob=p,enable_msg=False,latex=True)
