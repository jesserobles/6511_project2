



def no_inference(*args):
    return True

def forward_checking(csp, variable, value, assignment, removals=None):
    """Prune neighbor values inconsistent with var=value.
    Whenever a variable X is assigned, the forward-checking process establishes arc consistency 
    for it: for each unassigned variable Y that is connected to X by a constraint, delete from 
    Y's domain any value that is inconsistent with the value chosen for X
    """
    consistent = True
    csp.add_assignment(variable, value)
    assignment[variable] = value
    for neighbor in csp.neighbors[variable]:
        if neighbor not in assignment: # Only consider unassigned variables
            # for domain_value in csp.current_domains[neighbor]: # Iterate through the neighbors available domains
            for constraint in csp.constraints[neighbor]:
                # Check if the assignment is consistent with the current domain value
                if not constraint.is_satisfied({variable: value, neighbor: value}):
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
            if len(csp.domains[xi]) == 0:
                return False # CSP is inconsistent
            for xk in csp.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True # CSP is consistent

def revise(csp, xi, xj):
    """
    Method to remove inconsistent values from the domain of xi given the assignment (xi, xj)
    Returns True if the domain is revised, False otherwise
    """
    removed = False
    for x in csp.current_domains[xi]:
        # if no value y in DOMAIN[Xj] allows (x,y) to satisfy the constraint Xi <-> Xj
        if not any(csp.is_consistent(x, {x: y}) for y in csp.current_domains[xj]):
            # Delete x from DOMAIN[Xi]; removed <- true
            csp.current_domains[xi].remove(x)
            removed = True
    return removed


def maintain_arc_consistency(csp, variable, assignment, removals=None, constraint_propagation=ac3):
    """Maintain arc consistency."""
    return constraint_propagation(csp, queue={(x, variable) for x in csp.neighbors[variable]}, removals=removals)