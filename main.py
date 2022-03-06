from datetime import timedelta
import os
from time import time

from backtracking import backtracking_search
from graphcoloring import GraphColoringCSP

filepath = os.path.join("assets", "input_files", "gc_1377121623225900.txt")
start = time()
csp = GraphColoringCSP.from_file(filepath)
end = time()
print(f"Loaded file {filepath} in {timedelta(seconds=end-start)}")

start = time()
solution = backtracking_search(csp)
end = time()
print(f"Found solution in {timedelta(seconds=end-start)}")
print(solution)