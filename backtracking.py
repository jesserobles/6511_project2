from constraint import CSPBase
from ac3 import ac3

"""
The functions in this modules are based on the algorithms as described in the textbook:
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



def inference(csp, variable, assignment):
    return True

def select_unassigned_variable(csp, assignment):
    """
    Method to return an assignment.
    Simplest method is to just return the first unassigned variable.
    TODO: 
        - Incorporate MRV: choosing the variable with the fewest "legal" values
        - Incorporate degree heuristic: selecting the variable that is involved in the largest number of constraints on other unassigned variables
    """
    unassigned_variables = [variable for variable in csp.variables if variable not in assignment]
    return unassigned_variables[0]

def order_domain_values(csp, variable, assignment):
    """
    Method to order the values.
    Simplest method is to just return the values in whatever order they are in.
    TODO:
        - Incorporate LCV: choose the value that rules out the fewest choices for the neighboring variables in the constraint graph
    """
    domain_values = csp.domains[variable]
    return domain_values

def backtracking_search(csp: CSPBase):
    return backtrack(csp, {})

def backtrack(csp, assignment: dict, select_unassigned_variable=select_unassigned_variable, order_domain_values=order_domain_values, inference=inference):
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
            assignment[variable] = value
            # inferences <- INFERENCE(csp, var, assignment)
            # inferences = inference(csp, variable, assignment)
            inferences = ac3(csp)
            # if inferences != failure then
            if inferences:
                # add inferences to csp
                pass
                result = backtrack(csp, assignment)
                if result:
                    return result
                pass
            # remove {var = value} from assignment
            del assignment[variable]
    return None