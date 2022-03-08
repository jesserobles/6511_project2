from collections import defaultdict

"""
This module contains the inference functions and supporting utilities. These functions have the following signature:
    function(csp, variable, assignment)
returns either the string 'failure' if the resulting state is inconsistent, or a list of tuples representing deletions
from the domain where the first value is the variable and the second value is the value to be removed.
"""

def forward_checking(csp, variable, assignment):
    """Prune neighbor values inconsistent with var=value.
    Whenever a variable X is assigned, the forward-checking process establishes arc consistency 
    for it: for each unassigned variable Y that is connected to X by a constraint, delete from 
    Y's domain any value that is inconsistent with the value chosen for X
    """
    inferences = defaultdict(list)
    value = assignment[variable]
    for neighbor in csp.neighbors[variable]:
        if neighbor not in assignment: # Only consider unassigned variables
            for y in csp.domains[neighbor]: 
                # Check if the assignment is consistent with the current domain value
                if not csp.constraint_function(variable, value, neighbor, y):
                    inferences[neighbor].append(value)
            # if not csp.domains[neighbor]:
            if empty_domain(csp, neighbor, inferences):
                return 'failure'
    return inferences

def empty_domain(csp, variable, inferences):
    return len([value for value in csp.domains[variable] if not value in inferences[variable]]) == 0

def ac3(csp, queue=None):
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
    inferences = defaultdict(list)
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    while queue:
        xi, xj = queue.pop()
        revised = revise(csp, xi, xj)
        if revised:
            inferences[xi].extend(revised)
            if empty_domain(csp, xi, inferences):
                return 'failure'
            for xk in csp.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return inferences


def revise(csp, Xi, Xj):
    revised = []
    for x in csp.domains[Xi]:
        value_exists = False # if no value y in Dj allows (x,y) to satisfy the constraint between Xi and Xj
        for y in csp.domains[Xj]:
            if csp.constraint_function(Xi, x, Xj, y): # If this is true then a value exists, so no revision
                value_exists = True
                break
        if not value_exists: # No value satisfies the constraint, so remove it
            revised.append(x)
    return revised


def maintain_arc_consistency(csp, variable, assignment, constraint_propagation=ac3):
    """Maintain arc consistency."""
    queue = [(x, variable) for x in csp.neighbors[variable]]
    return constraint_propagation(csp, queue=queue)