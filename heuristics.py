"""
This module contains the variable and value ordering heuristics. The variable ordering heuristics have the signature
    function(csp, assignment)
and return the first value based on the ordering.
The value selection heuristic functions have the signature
    function(csp, variable, assignment)
and return a list of domain values sorted based on the ordering heuristic.
"""

# Heuristics for variable ordering

def static_ordering(csp, assignment):
    """
    Funtion to return an unassigned variable without ordering.
    Simplest method is to just return the first unassigned variable.
    """
    unassigned_variables = [variable for variable in csp.variables if variable not in assignment]
    return unassigned_variables[0]

def mrv(csp, assignment):
    """
    Implementation of the Minimum-Remaining-Values heuristic for ordering variables: 
        Choose the variable with the fewest remaining "legal" values.
    This implementation incorporates the tie breaking rule.
    """
    unassigned_variables = []
    for variable in csp.variables:
        if variable not in assignment:
            # Collecting the variable, number of remaining legal values (values left in domain), and how many constraints so we can sort
            unassigned_variables.append((variable,  len(csp.domains[variable]), -len(csp.constraints[variable])))
    # Sort by remaining legal values, then by how many constraints they have (tie breaker)
    unassigned_variables.sort(key=lambda x: (x[1], x[2]))
    return unassigned_variables[0][0]


# Heuristics for value ordering

def unordered_domain_values(csp, variable, assignment):
    """
    Function to return values without ordering them.
    Simplest method is to just return the values in whatever order they are in.
    """
    return csp.domains[variable]

def lcv(csp, variable, assignment):
    """
    Implementation of the Least Constraining Value heuristic to order values.
    We just sort by how many conflicts the assignment creates in ascending order.
    """
    return sorted(csp.domains[variable], key=lambda value: csp.count_conflicts(variable, value, assignment))
