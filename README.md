# Simplex Solver

Example code for solving linear equations using the simplex algorithm.

- Provides step-by-step instrucitons for Simplex algorithm.
- Outputs raw LaTeX file (WIP).

LaTeX files can be compiled [here].

### Examples

###### 1. Standard Maximization LP

Consider the following objective function and constraints:

<p align="center">
<img src="https://raw.githubusercontent.com/MichaelStott/SimplexSolver/master/img/example1a.png">
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/MichaelStott/SimplexSolver/master/img/example1b.png">
</p>
This problem can be solved by running the script with the following parameters:

```sh
$ python simplex.py -A "[[2,1],[1,2]]" -b "[4,3]" -c "[1,1]" -p "max"
```

License
----

MIT

[here]: <https://latexbase.com/>

