from collections import defaultdict, deque
from abc import ABC, abstractmethod
import queue
from typing import Dict, List, Set, Union

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
    properties:
        constraints: a mapping of variables to constraints, modified by the add_constraint method.
    """
    def __init__(self, variables: Union[List, Set], domains: Dict) -> None:
        self.variables = set(variables)
        self.domains = domains
        self.constraints: dict = defaultdict(list) # Equivalent to lazily instantiating each value as []
        self.arcs = self.get_arcs()
        self.assignment = {}

    def add_constraint(self, constraint: ConstraintBase) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise ValueError(f"Variable: {variable} not in constraint satisfaction problem.")
            self.constraints[variable].append(constraint)
    
    def is_consistent(self, variable, assignment: dict) -> bool:
        """Method to determine of an assignment is consistent with all of the constraints.
        variable: whatever the vertex represents (e.g., state in map coloring)
        assignment: a dictionary with format {0: 1, ...} where 0 is the vertex, and 1 is the assigned value (e.g., color)
        """
        for constraint in self.constraints[variable]:
            if not constraint.is_satisfied(assignment):
                return False
        return True
    
    def get_arcs(self):
        a = set([tuple(edge.variables) for edges in self.constraints.values() for edge in edges])
        a.update([(v[-1], v[0]) for v in a])
        return queue(a)

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
                    return result
        return None


