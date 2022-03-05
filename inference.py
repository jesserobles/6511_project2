from sortedcollections import SortedSet

"""
Inference methods have the following signature
inference(csp, variable, assignment) -> Returns true if inconsistency is found, true otherwise.
    Arguments:
        :csp: - A constraint satisfaction problem represented by a subclass of CSPBase
        :variable: - The variable being examined according to the SELECT-UNASSIGNED-VARIABLES method
        :assignment: - A dictionary with format {variable: value} containing the assignment thus far
    These methods may also update the domains of variables for a given assignment
"""


def no_inference(csp, variable, assignment, removals=None):
    consistent = True
    return consistent

def forward_checking(csp, variable, assignment, removals=None):
    """Prune neighbor values inconsistent with var=value.
    Whenever a variable X is assigned, the forward-checking process establishes arc consistency 
    for it: for each unassigned variable Y that is connected to X by a constraint, delete from 
    Y's domain any value that is inconsistent with the value chosen for X
    """
    consistent = True
    removals = removals or []
    # csp.add_assignment(variable, value)
    value = assignment[variable]
    for neighbor in csp.neighbors[variable]:
        if neighbor not in assignment: # Only consider unassigned variables
            for constraint in csp.constraints[neighbor]:# Iterate through the neighbors available domains
                # Check if the assignment is consistent with the current domain value
                if not constraint.is_satisfied({variable: value, neighbor: value}):
                    csp.prune(neighbor, value, removals) # remove inconsistent domain value
            if not csp.current_domains[neighbor]:
                consistent = False
    return consistent

# def ac3(csp, queue=None, removals=None):
#     """
#     Psuedocode from text/slides:

#     function AC-3(csp) returns the CSP, possibly with reduced domains
#         inputs: csp, a binary CSP with variables {X1, X2, ... , Xn}
#         local variables: queue, a queue of arcs, initially all the arcs in csp, subsequently only the arcs (Xj,Xi) for all Xj that are unassigned variables that are neighbors of Xi
#         while queue is not empty do
#             (Xi, Xj) <- REMOVE-FIRST(queue)
#             if REVISE(Xi, Xj) then
#             for each Xk in NEIGHBORS[Xi] do
#                 add (Xk, Xi) to queue
#     """
#     if queue is None:
#         queue = {(Xi, Xj) for Xi in csp.variables for Xj in csp.neighbors[Xi]}
#         queue.update({(Xj, Xi) for Xi in csp.variables for Xj in csp.neighbors[Xi]})
#     while queue:
#         xi, xj = queue.pop()
#         if revise(csp, xi, xj, removals):
#             if len(csp.current_domains[xi]) == 0:
#                 return False # CSP is inconsistent
#             for xk in csp.neighbors[xi]:
#                 if xk != xj:
#                     queue.add((xk, xi))
#     return True # CSP is consistent
def dom_j_up(csp, queue):
    return SortedSet(queue, key=lambda t: -(len(csp.current_domains[t[1]])))

def ac3(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    queue = arc_heuristic(csp, queue)
    while queue:
        (Xi, Xj) = queue.pop()
        revised= revise(csp, Xi, Xj, removals)
        if revised:
            if not csp.current_domains[Xi]:
                return False  # CSP is inconsistent
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True  # CSP is satisfiable

def revise(csp, Xi, Xj, removals=None):
    revised = False
    for x in csp.current_domains[Xi]:
        value_exists = False # if no value y in Dj allows (x,y) to satisfy the constraint between Xi and Xj
        for y in csp.current_domains[Xj]:
            if y != x:
                value_exists = True
                break
        if not value_exists:
            csp.prune(Xi, x)
            revised = True
    return revised


def maintain_arc_consistency(csp, variable, assignment, removals=None, constraint_propagation=ac3):
    """Maintain arc consistency.
    When using ac3: Instead of a queue of all arcs in the CSP, we start with only the arcs (Xj,Xi)
    for all Xj that are unassigned variables that are neighbors of Xi.
    """
    queue = {(X, variable) for X in csp.neighbors[variable]} # MAC just uses the neighbors instead of all arcs
    return constraint_propagation(csp, queue=queue, removals=removals)