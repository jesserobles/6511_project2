
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


def revise(csp: CSPBase, xi, xj):
    """
    Method to remove inconsistent values from the domain of xi given the assignment (xi, xj)
    """
    revised = False
    # di = csp.domains[xi].copy()
    for x in csp.domains[xi]:
        # if no value y in DOMAIN[Xj] allows (x,y) to satisfy the constraint Xi <-> Xj
        if not any(csp.is_consistent(x, {x: y}) for y in csp.domains[xj]):
            # Delete x from DOMAIN[Xi]; removed <- true
            csp.domains[xi] = [x_ for x_ in csp.domains[xi] if x_ != x]
            revised = True
    return revised


def get_neighbors(csp, vertex, exclude=set()):
    """
    Method to lazily generate the neighbors of a vertex.
    """
    for edge in csp.edges:
        if vertex in edge:
            v = [v for v in edge if v != vertex and not v in exclude]
            for v in edge:
                if v != vertex and not v in exclude:
                    yield v


def ac3(csp: CSPBase):
    """
    function AC-3(csp) returns the CSP, possibly with reduced domains
    inputs: csp, a binary CSP with variables {X1, X2, ... , Xn}
    local variables: queue, a queue of arcs, initially all the arcs in csp
    while queue is not empty do
        (Xi, Xj) <- REMOVE-FIRST( queue)
        if REVISE(Xi, Xj) then
        for each Xk in NEIGHBORS[Xi] do
            add (Xk, Xi) to queue
    """
    arcs = csp.arcs
    queue = deque(arcs)
    while queue:
        xi, xj = queue.popleft()
        if revise(csp, xi, xj):
            if len(csp.domains[xi]) == 0:
                return False
            for xk in get_neighbors(arcs, xi, exclude=set(xj)):
                queue.append((xk, xi))
    return True

def forward_check(csp, assignment: dict):
    vertex = list(assignment.keys())[0]
    domains = {}
    for neighbor in get_neighbors(csp, vertex):
        if csp.is_consistent(neighbor, assignment):
            pass