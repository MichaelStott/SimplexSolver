# Simplex Solver

Example code for solving linear equations using simplex.

- Provides step-by-step instrucitons for solving LPs using simplex algorithm (tableau method).
- Outputs raw LaTeX file.

LaTeX files can be compiled [here].

Note: Currently, only LPs in standard form are supported.

### Examples

###### 1. Standard Form Maximization LP

Consider the following objective function and constraints:

<p align="center">
<img src="https://raw.githubusercontent.com/MichaelStott/SimplexSolver/master/img/example1a.png">
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/MichaelStott/SimplexSolver/master/img/example1b.png">
</p>
This problem can be solved by running the script with the following parameters:

```sh
$ python simplex.py -A "[[2,1],[1,2]]" -b "[4,3]" -c "[1,1]" -p max
```

###### 2. Standard Form Minimization LP

Consider the following objective function and constraints:

<p align="center">
<img src="https://raw.githubusercontent.com/MichaelStott/SimplexSolver/master/img/example2a.png">
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/MichaelStott/SimplexSolver/master/img/example2b.png">
</p>
This problem can be solved by running the script with the following parameters:

```sh
$ python simplex.py -A "[[2,1],[1,1]]" -b "[6,4]" -c "[3,2]" -p min
```

[here]: <https://latexbase.com/>

