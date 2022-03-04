from collections import defaultdict, deque
from copy import deepcopy
from abc import ABC, abstractmethod
from typing import Dict, List, Set, Union

from sklearn import neighbors

from utils import count_trues

"""
TODO: Explore and implement the following CSP backtracking efficiency improvement methods:
Ordering:
    Variables:
        Most constrained variable (MCV) - Choose the variable with the fewest legal left values in its domain
        Tie breaking rule - consider a variable that is involved in more constraints
    Values:
        Least constraining value (LCV) - Choose the value that rules out the fewest values in the remaining variables

Filtering: Keep track of domains for unassigned variables and cross off bad options
Forward checking: Cross off values that violate a constraint when added to the existing assignment

AC-3 algorithm
Remember: Delete from the tail!
"""

class ConstraintBase(ABC):
    """Base class for constraints"""
    def __init__(self, variables: List) -> None:
        self.variables = variables

    @abstractmethod
    def is_satisfied(self, assignment):
        """Method should be overriden in subclasses"""
        pass


class CSPBase(ABC):
    """
    Base class for constrained satisfaction problems.
    args:
        variables: a list of variables
        domains: a dictionary mapping variables to possible values
        neighbors: a dictionary containing vertices as the keys and their neighbors as the values (adjacency list)
    properties:
        constraints: a mapping of variables to constraints, modified by the add_constraint method.
        current_domains: dictionary of remaining consistent values for each variable. This changes
            as the search traverses.
    """
    def __init__(self, variables: Union[List, Set], domains: Dict, neighbors:dict) -> None:
        self.variables = set(variables)
        self.domains = domains
        self.neighbors = neighbors
        self.constraints: dict = defaultdict(list) # Equivalent to lazily instantiating each value as []
        self.arcs = self.get_arcs()
        self.assignment = None
        self.current_domains = None
        self.assignment_counts = 0
        # self.current_domains = deepcopy(self.domains) # Initially this is the same as the domains, but varies during search
        # self.constraints_func = lambda A, a, B, b: a != b
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.assignment}>"
    
    def support_pruning(self):
        """Method to initialize the current domains during search"""
        if self.current_domains is None:
            self.current_domains = deepcopy(self.domains) # Initially this is the same as the domains, but varies during search

    def add_constraint(self, constraint: ConstraintBase) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise ValueError(f"Variable: {variable} not in constraint satisfaction problem.")
            self.constraints[variable].append(constraint)
    
    def is_consistent(self, variable, assignment: dict) -> bool:
        """
        Method to determine of an assignment is consistent with all of the constraints.
        variable: whatever the vertex represents (e.g., state in map coloring)
        assignment: a dictionary with format {variable: value, ...}, e.g., {0: 1} where 0 is a vertex
        and 1 is the color for a graph coloring problem. So if we assign {0:1}, we want to check if
        there are any constraints on `variable` that are not satisfied.
        """
        for constraint in self.constraints[variable]:
            if not constraint.is_satisfied(assignment):
                return False
        return True
    

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        removals = [(var, a) for a in self.current_domains[var] if a != value]
        self.current_domains[var] = [value]
        return removals

    def assign(self, variable, value, assignment):
        assignment[variable] = value
        self.assignment_counts += 1

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.current_domains[B].append(b)

    def choices(self, variable):
        """Return all values for var that aren't currently ruled out."""
        return (self.current_domains or self.domains)[variable]

    def get_arcs(self):
        a = set([tuple(edge.variables) for edges in self.constraints.values() for edge in edges])
        a.update([(v[-1], v[0]) for v in a])
        return deque(a)
    
    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.current_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))
    
    def count_conflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables already assigned (in assignment)
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values {A:a}, {B:b}
        """
    
        # We are checking if assigning var = val will cause csp.is_consistent to return False
        count = 0
        temp_assignment = assignment.copy()
        temp_assignment[var] = val
        for v in self.neighbors[var]: # iterate through the neighbors of var    
            if v in assignment and not self.is_consistent(v, temp_assignment): # Check if the assignment causes any conflicts with 
                count += 1
        return count

    # def nconflicts(self, var, val, assignment):
    #     """Return the number of conflicts var=val has with other variables."""

    #     # Subclasses may implement this more efficiently
    #     def conflict(var2):
    #         return var2 in assignment and not self.constraints_func(var, val, var2, assignment[var2])
    #     return count_trues([v in assignment and not self.constraints_func(var, val, v, assignment[v]) for v in self.neighbors[var]])
    
    def backtracking_search(self, assignment: dict = {}):
        """
        Recursive backtracking search algorithm
        """
        if len(self.variables) == len(assignment):
            # Base case. All assignments have been done, return it
            return assignment
        # Otherwise, we handle the unassigned variables
        unassigned_variables = [variable for variable in self.variables if variable not in assignment]
        first_unassigned = unassigned_variables[0]
        # Loop through the values in the first unassigned variable's domain
        for value in self.domains[first_unassigned]:
            # Try assigning the value to each variable.
            # First make a copy of the assignment, then set the value
            temp_assignment = assignment.copy()
            temp_assignment[first_unassigned] = value
            # Check if assignment is consistent
            if self.is_consistent(first_unassigned, temp_assignment):
                # If consistent continue searching using the assignment
                result = self.backtracking_search(temp_assignment)
                if result is not None:
                    self.assignment = result
                    return result
        return None


