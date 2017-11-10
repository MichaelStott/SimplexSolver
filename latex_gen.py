import ast, getopt, sys, copy
from latex import build_pdf

from simplex import SimplexSolver

def start(latex_str):
    latex_str = (r"\documentclass{article}")
        
    latex_str += (r"\begin{document}")
    latex_str += (r"\title{Simplex Solver}")
    latex_str += (r"\maketitle")
    latex_str += (r"\begin{flushleft}")
    latex_str += (r"\textbf{Problem}")
    latex_str += (r"\end{flushleft}")
    latex_str += (r"\begin{flushleft}")
    latex_str += (r"Given the following linear system and objective function, "
                  r"find the optimal solution.")
    latex_str += (r"\end{flushleft}")
    return latex_str

def obj_func(latex_str, c):
    latex_str += (r"\begin{equation}")
    func = ""
    found_value = False
    for index, x in enumerate(c):
        opp = '+'
        if x == 0:
            continue
        if x < 0:
            opp = ' - '
        elif index == 0 or not found_value:
            opp = ''
        if x == 1 or x == -1:
            x = ''
        func += (r"%s %sx_%s "  % (opp, str(x), str(index)))
        found_value = True
    latex_str += (r"\max{%s}" % func)
    latex_str += (r"\end{equation}")
    return latex_str

def eq_from_mat(latex_str, A):
    latex_str += (r"\[")
    latex_str += (r"\left\{")
    latex_str += (r"\begin{array}{c}")
    for i in range(0, len(A)):
        found_value = False
        for index, x in enumerate(A[i]):
            opp = '+'
            if x == 0 and index != len(A[i]) - 1:
                continue
            if x < 0:
                opp = '-'
            elif index == 0 or not found_value:
                opp = ''
            if index != len(A[i]) - 1:
                if x == 1 or x == -1:
                    x = ''
                latex_str += (r"%s %sx_%s "  % (opp, str(x), str(index)))
            else:
                latex_str += (r"= %s"  % str(x))
            found_value = True
            if (index == len(A[i]) - 1):
                latex_str += r" \\ "        
    latex_str += (r"\end{array}")
    latex_str += (r"\right.")
    latex_str += (r"\]")
    return latex_str

if __name__ == '__main__':

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

    latex_str = eq_from_mat(obj_func(start(''), ss.c), ss.get_Ab()) +\
                (r"\begin{flushleft}") +\
                (r"\textbf{Solution}") +\
                (r"\end{flushleft}")

    latex_str += (r"\begin{flushleft}")
    latex_str += (r"Add slack and artificial variables to turn "
                  r"all inequalities to equalities.")
    latex_str += (r"\end{flushleft}")
    latex_str = eq_from_mat(latex_str, ss.tableau)
    latex_str += (r"\begin{flushleft}")
    latex_str += (r"Thus, the initial tableau is as follows.")
    latex_str += (r"\end{flushleft}")
    
    latex_str += (r"\end{document}")
    pdf = build_pdf(latex_str)
    pdf.save_to('solution.pdf')

