

def count_trues(sequence):
    """Count the number of true items in sequence."""
    return sum(map(bool, sequence))
    
def check_solution(csp, assignment):
    # First make sure all values are assigned
    if len(assignment) != len(csp.variables):
        return False
    # Now loop through the assignments, check if there are any conflicts
    for variable in csp.variables:
        if csp.count_conflicts(variable, assignment[variable], assignment) != 0:
            return False
    return True

def goal_test(csp, state):
    """The goal is to assign all variables, with all constraints satisfied."""
    assignment = dict(state)
    return (len(assignment) == len(csp.variables)
            and all(csp.count_conflicts(variables, assignment[variables], assignment) == 0
                    for variables in csp.variables))
