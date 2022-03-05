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

# def mrv(csp, assignment):
#     """Minimum-remaining-values heuristic: Choose the variable with the fewest remaining "legal" values"""
#     unassigned_variables = sorted(
#         [(variable,  remaining_legal_values(csp, variable, assignment), -len(csp.constraints[variable])) for variable in csp.variables if variable not in assignment],
#         key=lambda x: (x[1], x[2])
#     )
#     return unassigned_variables[0][0]


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


def shuffled(iterable):
    """Randomly shuffle a copy of iterable."""
    items = list(iterable)
    random.shuffle(items)
    return items

def argmin_random_tie(seq, key=lambda x: x):
    """Return a minimum element of seq; break ties at random."""
    return min(shuffled(seq), key=key)

def remaining_legal_values(csp, variable, assignment):
    """
    Method to return the number of remaining legal values
    """
    if csp.current_domains:
        return len(csp.current_domains[variable])
    else:
        return count_trues(csp.count_conflicts(variable, value, assignment) == 0 for value in csp.domains[variable])

def mrv(csp, assignment):
    """Minimum-remaining-values heuristic."""
    return argmin_random_tie([v for v in csp.variables if v not in assignment],
                             key=lambda var: remaining_legal_values(csp, var, assignment))

