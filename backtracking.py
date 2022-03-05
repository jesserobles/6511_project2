from sortedcollections import SortedSet

from heuristics import static_ordering, mrv, lcv
from inference import maintain_arc_consistency

"""
The functions in this modules are based on the algorithms as described in class
slides and in the textbook:
Artificial Intelligence: A Modern Approach (Prentice Hall 2020)

function BACKTRACKING-SEARCH(csp) returns a solution or failure
    return BACKTRACK(csp, {})

function BACKTRACK(csp, assignment) returns a solution or failure
    if assignment is complete then return assignment
    var <- SELECT-UNASSIGNED-VARIABLE(csp, assignment)
    for each value in ORDER-DOMAIN-VALUES(csp, var, assignment) do
        if value is consistent with assignment then
            add {var = value} to assignment
            inferences <- INFERENCE(csp, var, assignment)
            if inferences != failure then
                add inferences to csp
                result <- BACKTRACK(csp, assignment)
                if result != failure then return result
                remove inferences from csp
            remove {var = value} from assignment
    return failure
"""



def dom_j_up(csp, queue):
    """Order by increasing size of the domain of the variables"""
    return SortedSet(queue, key=lambda t: -len(csp.current_domains[t[1]]))


# def backtracking_search(csp, verbose=True, select_unassigned_variable=mrv, order_domain_values=lcv, inference=maintain_arc_consistency):
#     if verbose:
#         print_problem(select_unassigned_variable, order_domain_values, inference)
#     return backtrack(csp, {}, select_unassigned_variable=select_unassigned_variable, order_domain_values=order_domain_values, inference=inference)

# def backtrack(csp, assignment, select_unassigned_variable, order_domain_values, inference):
#     # if assignment is complete then return assignment
#     if csp.is_complete(assignment): return assignment # Base case
#     # var <- SELECT-UNASSIGNED-VARIABLE(csp, assignment)
#     variable = select_unassigned_variable(csp, assignment)
#     # for each value in ORDER-DOMAIN-VALUES(csp, var, assignment) do
#     for value in order_domain_values(csp, variable, assignment):
#         # if value is consistent with assignment then
#         if csp.is_consistent(variable, assignment):
#             # add {var = value} to assignment
#             csp.assign(variable, value, assignment)
#             removals = csp.add_assignment(variable, value) # Keep track of removals in case we need to restore them
#             # inferences <- INFERENCE(csp, var, assignment)
#             inferences = inference(csp, variable, assignment, removals)
#             # if inferences != failure then
#             if inferences:
#                 print("Backtracking")
#                 # add inferences to csp -> These were already added via the inference method
#                 result = backtrack(csp, assignment, select_unassigned_variable, order_domain_values, inference)
#                 # if result != failure then return result
#                 if result: return result
#                 # remove inferences from csp
#                 print("Restoring")
#             csp.restore(removals)
#             # remove {var = value} from assignment
#     csp.unassign(variable, assignment)
#     return None
def backtrack(csp, assignment, select_unassigned_variable=mrv,
                        order_domain_values=lcv, inference=maintain_arc_consistency):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(csp, assignment)
        for value in order_domain_values(csp, var, assignment):
            if 0 == csp.count_conflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.add_assignment(var, value)
                if inference(csp, var, assignment, removals):
                    result = backtrack(csp, assignment, select_unassigned_variable=mrv,
                        order_domain_values=lcv, inference=maintain_arc_consistency)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

def backtracking_search(csp, select_unassigned_variable=mrv,
                        order_domain_values=lcv, inference=maintain_arc_consistency):
    """[Figure 6.5]"""

    result = backtrack(csp, {}, select_unassigned_variable=select_unassigned_variable, 
        order_domain_values=order_domain_values, inference=inference)
    # assert result is None or csp.goal_test(result)
    return result

def print_problem(variable_heuristic, value_heuristic, inference):
    for type_, function in {"Variable ordering heuristic": variable_heuristic, "Value ordering heuristic": value_heuristic, "Inference type": inference}.items():
        print(f"{type_} -> {function.__name__}")
    print()