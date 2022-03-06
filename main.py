from datetime import timedelta
import os
from time import time

from backtracking import backtracking_search
from graphcoloring import GraphColoringCSP
from heuristics import lcv, mrv, static_ordering, unordered_domain_values
from inference import forward_checking, maintain_arc_consistency

def solve(input_file, **kwargs):
    csp = GraphColoringCSP.from_file(input_file)
    start = time()
    solution = backtracking_search(csp, 
        select_unassigned_variable=kwargs['select_unassigned_variable'],
        order_domain_values=kwargs['order_domain_values'],
        inference=kwargs['inference']
    )
    end = time()
    print(f'\nElapsed time: {timedelta(seconds=end-start)}\n')
    return solution

if __name__ == "__main__":
    import argparse
    import glob
    import json

    parser = argparse.ArgumentParser(description="Graph Coloring CSP search solver.")
    parser.add_argument('file',
                    help='Graph coloring CSP input files as described in the project assignment',
                    default='*')
    parser.add_argument('-var', '--variableorder',
                    choices=['mrv', 'static', 'none'],
                    help="Variable ordering heuristic",
                    default="mrv")
    parser.add_argument('-val', '--valueeorder',
                    choices=['lcv', 'unordered', 'none'],
                    help="Value ordering heuristic",
                    default="lcv")
    parser.add_argument('-inf', '--inference',
                    choices=['mac', 'fc'],
                    help="Inference method",
                    default="mac")
    
    args = parser.parse_args()

    variable_ordering_functions = {
        'mrv': mrv,
        'static': static_ordering,
        'none': static_ordering
    }

    value_ordering_functions = {
        'lcv': lcv,
        'unordered': unordered_domain_values,
        'none': unordered_domain_values
    }

    inference_methods = {
        'fc': forward_checking,
        'mac': maintain_arc_consistency
    }

    file = args.file
    select_unassigned_variable = variable_ordering_functions.get(args.variableorder)
    order_domain_values = value_ordering_functions.get(args.valueeorder)
    inference = inference_methods.get(args.inference)

    if file == '*':
        folder = os.path.join("assets", "input_files")
        for file in os.listdir(folder):
            # Skip large file
            if 'gc_1377121623225900.txt' in file:
                continue
            solution = solve(os.path.join(folder, file), 
                select_unassigned_variable=select_unassigned_variable,
                order_domain_values=order_domain_values,
                inference=inference)
            if solution:
                print(f"\nSolution for file {os.path.basename(file)} -> {json.dumps(solution)}\n")
            else:
                print(f"\nSolution for file {os.path.basename(file)} -> No solution found.\n")
    else:
        solution = solve(file, 
            select_unassigned_variable=select_unassigned_variable,
            order_domain_values=order_domain_values,
            inference=inference)
        if solution:
            print(f"\nSolution for file {os.path.basename(file)} -> {json.dumps(solution)}\n")
        else:
            print(f"\nSolution for file {os.path.basename(file)} -> No solution found.\n")
