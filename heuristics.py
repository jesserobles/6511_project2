import random

from utils import count_trues

# Heuristics for variable ordering

def static_ordering(csp, assignment):
    """
    Method to return an assignment.
    Simplest method is to just return the first unassigned variable.
    TODO: 
        - Incorporate MRV: choosing the variable with the fewest "legal" values
        - Incorporate degree heuristic: selecting the variable that is involved in the largest number of constraints on other unassigned variables
    """
    unassigned_variables = [variable for variable in csp.variables if variable not in assignment]
    return unassigned_variables[0]

def mrv(csp, assignment):
    """
    Minimum-remaining-values heuristic: Choose the variable with the fewest remaining "legal" values.
    This incorporates the tie breaking rule.
    """
    unassigned_variables = []
    for variable in csp.variables:
        if variable not in assignment:
            unassigned_variables.append((variable,  remaining_legal_values(csp, variable, assignment), -len(csp.constraints[variable])))
    # unassigned_variables = sorted(
    #     [(variable,  remaining_legal_values(csp, variable, assignment), -len(csp.constraints[variable])) for variable in csp.variables if variable not in assignment],
    #     key=lambda x: (x[1], x[2])
    # )
    unassigned_variables.sort(key=lambda x: (x[1], x[2]))
    return unassigned_variables[0][0]


# Heuristics for value ordering

def unordered_domain_values(csp, variable, assignment):
    """
    Method to order the values.
    Simplest method is to just return the values in whatever order they are in.
    TODO:
        - Incorporate LCV: choose the value that rules out the fewest choices for the neighboring variables in the constraint graph
    """
    domain_values = (csp.current_domains or csp.domains)[variable]
    return domain_values

def lcv(csp, variable, assignment):
    """
    Least constraining value heuristic.
    """
    return sorted(csp.current_domains[variable], key=lambda value: csp.count_conflicts(variable, value, assignment))

def remaining_legal_values(csp, variable, assignment):
    """
    Method to return the number of remaining legal values
    """
    if csp.current_domains:
        return len(csp.current_domains[variable])
    else:
        return count_trues(csp.count_conflicts(variable, value, assignment) == 0 for value in csp.domains[variable])

