from sortedcollections import SortedSet

from constraint import CSPBase
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
                result←BACKTRACK(csp, assignment)
                if result != failure then return result
                remove inferences from csp
            remove {var = value} from assignment
    return failure
"""



def dom_j_up(csp, queue):
    """Order by increasing size of the domain of the variables"""
    return SortedSet(queue, key=lambda t: -len(csp.current_domains[t[1]]))


def backtracking_search(csp: CSPBase, select_unassigned_variable=mrv, order_domain_values=lcv, inference=maintain_arc_consistency):
    csp.support_pruning()
    print_problem(select_unassigned_variable, order_domain_values, inference)
    return backtrack(csp, {}, select_unassigned_variable=select_unassigned_variable, order_domain_values=order_domain_values, inference=inference)

def backtrack(csp, assignment: dict, select_unassigned_variable, order_domain_values, inference):
    # if assignment is complete then return assignment
    if len(assignment) == len(csp.variables): # Base case
        return assignment
    # var <- SELECT-UNASSIGNED-VARIABLE(csp, assignment)
    variable = select_unassigned_variable(csp, assignment)
    # for each value in ORDER-DOMAIN-VALUES(csp, var, assignment) do
    for value in order_domain_values(csp, variable, assignment):
        # if value is consistent with assignment then
        temp_assignment = assignment.copy()
        temp_assignment[variable] = value
        if csp.is_consistent(variable, temp_assignment):
            # add {var = value} to assignment
            csp.assign(variable, value, assignment)
            removals = csp.add_assingment(variable, value)
            # inferences <- INFERENCE(csp, var, assignment)
            inferences = inference(csp, variable, assignment)
            # if inferences != failure then
            if inferences:
                # add inferences to csp
                result = backtrack(csp, assignment, select_unassigned_variable, order_domain_values, inference)
                if result:
                    return result
            # remove {var = value} from assignment
            csp.restore(removals)
            del assignment[variable]
    return None

def print_problem(variable_heuristic, value_heuristic, inference):
    for type_, function in {"Variable ordering heuristic": variable_heuristic, "Value ordering heuristic": value_heuristic, "Inference type": inference}.items():
        print(f"{type_} -> {function.__name__}")
    print()