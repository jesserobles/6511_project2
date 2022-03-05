import os

from graphcoloring import GraphColoringCSP
from heuristics import lcv, mrv
from inference import ac3, forward_checking, maintain_arc_consistency, no_inference, revise
from backtracking import backtracking_search

csp = GraphColoringCSP.from_file(os.path.join("assets", "input_files", "australia.txt"))
csp = GraphColoringCSP.from_file(os.path.join("assets", "input_files", "gc_78317097930400.txt"))
backtracking_search(csp)


select_unassigned_variable = mrv
order_domain_values = lcv
inference = maintain_arc_consistency
inference = forward_checking
assignment = {}
variable = select_unassigned_variable(csp, assignment)

values = order_domain_values(csp, variable, assignment)
value = values[0]

csp.assign(variable, value, assignment)
removals = csp.add_assignment(variable, value)
inferences = inference(csp, variable, assignment, removals)

# # if assignment is complete then return assignment
# if csp.is_complete(assignment): return assignment # Base case
# # var <- SELECT-UNASSIGNED-VARIABLE(csp, assignment)
# variable = select_unassigned_variable(csp, assignment)
# # for each value in ORDER-DOMAIN-VALUES(csp, var, assignment) do
# for value in order_domain_values(csp, variable, assignment):
#     # if value is consistent with assignment then
#     if csp.is_consistent(variable, assignment):
#         # add {var = value} to assignment
#         csp.assign(variable, value, assignment)
#         removals = csp.add_assignment(variable, value) # Keep track of removals in case we need to restore them
#         # inferences <- INFERENCE(csp, var, assignment)
#         inferences = inference(csp, variable, assignment, removals)
#         # if inferences != failure then
#         if inferences:
#             # add inferences to csp -> These were already added via the inference method
#             result = backtrack(csp, assignment, select_unassigned_variable, order_domain_values, inference)
#             # if result != failure then return result
#             if result: return result
#             # remove inferences from csp
#             csp.restore(removals)
#         # remove {var = value} from assignment
#         csp.unassign(variable, assignment)



