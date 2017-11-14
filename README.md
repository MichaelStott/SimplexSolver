# Simplex Solver

Example code for solving linear equations using the simplex algorithm.

  - Provides step-by-step instrucitons for Simplex algorithm.
  - Outputs raw LaTeX file (WIP).

LaTeX files can be compiled [here].

### Example

Consider the following objective function and constraints:

This problem can be solved using the script 
```sh
$ python simplex.py -A "[[2,1],[1,2]]" -b "[4,3]" -c "[1,1]"
```

### Todos

 - Include support for LPs in nonstandard form.
 - Include more unit test cases.
 - Integrate LaTeX generation into simplex.py

License
----

MIT

   [here]: <https://latexbase.com/>