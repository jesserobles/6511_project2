from collections import deque

from constraint import CSPBase
"""
function AC-3(csp) returns the CSP, possibly with reduced domains
    inputs: csp, a binary CSP with variables {X1, X2, ... , Xn}
    local variables: queue, a queue of arcs, initially all the arcs in csp
    while queue is not empty do
        (Xi, Xj) <- REMOVE-FIRST( queue)
        if REVISE(Xi, Xj) then
        for each Xk in NEIGHBORS[Xi] do
            add (Xk, Xi) to queue


function REVISE(Xi, Xj) returns true iff succeeds
    removed <- false
    for each x in DOMAIN[Xi] do
        if no value y in DOMAIN[Xj] allows (x,y) to satisfy the constraint Xi <-> Xj
            then delete x from DOMAIN[Xi]; removed <- true
    return removed
"""

def ac3(csp: CSPBase, queue=None, removals=None):
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
    print(f"Queue length: {len(queue)}")
    while queue:
        xi, xj = queue.pop()
        if revise(csp, xi, xj):
            if len(csp.domains[xi]) == 0:
                return False # CSP is inconsistent
            for xk in csp.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True # CSP is consistent

def revise(csp: CSPBase, xi, xj):
    """
    Method to remove inconsistent values from the domain of xi given the assignment (xi, xj)
    """
    revised = False
    # di = csp.domains[xi].copy()
    for x in csp.current_domains[xi]:
        # if no value y in DOMAIN[Xj] allows (x,y) to satisfy the constraint Xi <-> Xj
        if not any(csp.is_consistent(x, {x: y}) for y in csp.current_domains[xj]):
            # Delete x from DOMAIN[Xi]; removed <- true
            # csp.current_domains[xi] = [x_ for x_ in csp.current_domains[xi] if x_ != x]
            csp.current_domains[xi].remove(x)
            revised = True
    return revised


def forward_check(csp, assignment: dict):
    vertex = list(assignment.keys())[0]
    domains = {}
    for neighbor in csp.neighbors[vertex]:
        if csp.is_consistent(neighbor, assignment):
            pass

