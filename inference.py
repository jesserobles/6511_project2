
def no_inference(*args):
    return True

def forward_checking(csp, variable, assignment, removals=None):
    """Prune neighbor values inconsistent with var=value.
    Whenever a variable X is assigned, the forward-checking process establishes arc consistency 
    for it: for each unassigned variable Y that is connected to X by a constraint, delete from 
    Y's domain any value that is inconsistent with the value chosen for X
    """
    consistent = True
    removals = removals or []
    value = assignment[variable]
    for neighbor in csp.neighbors[variable]:
        if neighbor not in assignment: # Only consider unassigned variables
            for y in csp.current_domains[neighbor]: 
                # Check if the assignment is consistent with the current domain value
                if not csp.constraint_function(variable, value, neighbor, y):
                    csp.prune(neighbor, value, removals) # remove inconsistent domain value
            if not csp.current_domains[neighbor]:
                consistent = False
    return consistent

def ac3(csp, queue=None, removals=None):
    """
    Psuedocode from text/slides:

    function AC-3(csp) returns the CSP, possibly with reduced domains
        inputs: csp, a binary CSP with variables {X1, X2, ... , Xn}
        local variables: queue, a queue of arcs, initially all the arcs in csp, subsequently only the arcs (Xj,Xi) for all Xj that are unassigned variables that are neighbors of Xi
        while queue is not empty do
            (Xi, Xj) <- REMOVE-FIRST(queue)
            if REVISE(Xi, Xj) then
            for each Xk in NEIGHBORS[Xi] do
                add (Xk, Xi) to queue
    """
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    while queue:
        xi, xj = queue.pop()
        if revise(csp, xi, xj):
            if len(csp.current_domains[xi]) == 0:
                return False # CSP is inconsistent
            for xk in csp.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True # CSP is consistent


def revise(csp, Xi, Xj, removals=None):
    revised = False
    for x in csp.current_domains[Xi]:
        value_exists = False # if no value y in Dj allows (x,y) to satisfy the constraint between Xi and Xj
        for y in csp.current_domains[Xj]:
            if csp.constraint_function(Xi, x, Xj, y): # If this is true then a value exists, so no revision
                value_exists = True
                break
        if not value_exists: # No value satisfies the constraint, so remove it
            csp.prune(Xi, x)
            revised = True
    return revised


def dom_j_up(csp, queue):
    return sorted(queue, key=lambda t: -(len(csp.current_domains[t[1]])))

def maintain_arc_consistency(csp, variable, assignment, removals=None, constraint_propagation=ac3, ordering_heuristic=None):
    """Maintain arc consistency."""
    queue = [(x, variable) for x in csp.neighbors[variable]]
    # queue.extend([(variable, x) for x in csp.neighbors[variable]])
    if ordering_heuristic:
        queue = ordering_heuristic(csp, queue)
    return constraint_propagation(csp, queue=queue, removals=removals)