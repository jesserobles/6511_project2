from collections import defaultdict
from abc import ABC, abstractmethod
from typing import Dict, List, Set, Union


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
        variables: a list of variables (vertices)
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
        self.assignment_counts = 0

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} -> vars: {len(self.variables)}, domains: {len(self.domains)}>"
    
    @abstractmethod
    def constraint_function(self, *args):
        """
        Override this method to specify the CSP constraint.
        """
        pass

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

    def add_assignment(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        removals = [(var, a) for a in self.domains[var] if a != value]
        self.domains[var] = [value]
        return removals
    
    def add_assignments(self, assignments):
        removals = []
        for var, value in assignments.items():
            removals.append(self.add_assignment(var, value))
        return removals

    def assign(self, variable, value, assignment):
        assignment[variable] = value
        self.assignment_counts += 1

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.domains[B].append(b)
    
    def add_inferences(self, inferences):
        for variable, values in inferences.items():
            for value in values:
                self.domains[variable].remove(value)

    def remove_inferences(self, inferences):
        for variable, values in inferences.items():
            for value in values:
                self.domains[variable].append(value)

    def prune(self, var, value, removals=None):
        """Rule out var=value."""
        self.domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))
    
    def count_conflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables already assigned (in assignment)
        """
    
        # We are checking if assigning var = val will cause csp.is_consistent to return False
        count = 0
        temp_assignment = assignment.copy()
        temp_assignment[var] = val
        for v in self.neighbors[var]: # iterate through the neighbors of var    
            if v in assignment and not self.is_consistent(v, temp_assignment): # Check if the assignment causes any conflicts with a neighbor
                count += 1
        return count
    
    def valid_solution(self, assignment):
        """The goal is to assign all variables, with all constraints satisfied."""
        if not assignment:
            return False
        return (len(assignment) == len(self.variables)
                and all(self.count_conflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))
