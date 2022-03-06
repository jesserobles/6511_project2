# Graph Coloring CSP

This repo contains the code for CS6511 Project 2 for Spring 2022. There are several example input files in the `assets/input_files` folder.

# Running the code on an input file

To run the code on an input file, run `python main.py filepath`, replacing filepath with the relative path to the input file (e.g., `assets/input_files/australia.txt`). Running the command without the filepath argument will run the graph coloring CSP backtracking on all but the largest input file and print out the solution and elapsed time. You can also pass additional arguments for variable and value ordering and inference method.

# Running unit tests
To run unit tests, run `python unittests.py`. This will simply print out how many tests it ran, and `OK` if all tests passed, and `FAILURE` and cause of the failure(s) otherwise. The unit tests test out the different variable and value ordering heuristics (mrv, lcv), inference methods (forward checking, maintaining arc consistency with ac3), and backtracking search for several combinations of these.