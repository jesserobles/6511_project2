# Graph Coloring CSP

This repo contains the code for CS6511 Project 2 for Spring 2022. There are several example input files in the `assets/input_files` folder, which were taken from the example files located in the class [repo](https://github.com/amrinderarora/ai/tree/master/src/main/resources/csp/coloring).

# Running the code on an input file

To run the code on an input file, run `python main.py filepath`, replacing filepath with the relative path to the input file (e.g., `assets/input_files/australia.txt`). Running the command with `*` as the filepath argument will run the graph coloring CSP backtracking on all but the largest input file and print out the solution and elapsed time. You can also pass additional arguments for variable and value ordering and inference method, as described in the help:
```bash
positional arguments:
  file                  Graph coloring CSP input files as described in the project assignment

optional arguments:
  -h, --help            show this help message and exit
  -var {mrv,static,none}, --variableorder {mrv,static,none}
                        Variable ordering heuristic
  -val {lcv,unordered,none}, --valueeorder {lcv,unordered,none}
                        Value ordering heuristic
  -inf {mac,fc,none}, --inference {mac,fc,none}
                        Inference method
```
### A note on file `gc_1377121623225900.txt`
This large file is excluded from the unit tests and the default `main.py` execution because it takes a very long time to run, even using the mrv and lcv heuristics and maintaining arc consistency. I ran this file, and it took `1:54:36.671057` and the search found no solution.

# Running unit tests
To run unit tests, run `python unittests.py`. This will simply print out how many tests it ran, and `OK` if all tests passed, and `FAILURE` and cause of the failure(s) otherwise. The unit tests test out the different variable and value ordering heuristics (mrv, lcv), inference methods (forward checking, maintaining arc consistency with ac3), and backtracking search for several combinations of these.

# Module Layout
This repo is organized into several modules that implement different parts of the graph coloring constraint satisfaction problem so that the layout hopefully makes sense. The `fileparser.py` module contains a class that parses an input file so it can be loaded and represented as a CSP. The `graphcoloring.py` file contains the `GraphColoringCSP` and `GraphColoringConstraint` classes. These classes contains attributes such as `neighbors` and `domains` as well as methods such as `is_consistent`, `count_conflicts`, `add_inferences`, and `remove_inferences` to help us implement the heuristics and inference methods, as well as the backtracking algorithm. In essence, the a `GraphColoringCSP` object represents `csp` in the pseudocode. The `heuristics.py` module contains the variable ordering heuristics (static and mrv) as well as the value ordering heuristics (unordered, lcv). The `inference.py` module contains the inference methods forward checking and maintaining arc consistency using ac3. The `backtracking.py` file contains the implementation of the backtracking algorithm. The `unittests.py` module contains unit tests and can be run as described above in the **Running unit tests**. The `main.py` module is the main entrypoint to run the backtracking search on input files, as described above in the **Running the code on an input file** section.