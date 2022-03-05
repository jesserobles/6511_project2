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



