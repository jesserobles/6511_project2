from collections import defaultdict
from abc import ABC, abstractmethod
from typing import Dict, Generic, List


class ConstraintBase(ABC):
    """Base class for constraints"""
    def __init__(self, variables: List) -> None:
        self.variables = variables

    @abstractmethod
    def is_satisfied(self, assignment: dict)->bool:
        pass


class ConstrainedSatisfactionProblemBase(ABC):
    """
    Base class for constrained satisfaction problems.
    args:
        variables: a list of variables
        domains: a dictionary mapping variables to possible values
    properties:
        constraints: a mapping of variables to constraints, modified by the add_constraint method.
    """
    def __init__(self, variables: List, domains: Dict) -> None:
        self.variables = variables
        self.domains = domains
        self.constraints = defaultdict(list) # Equivalent to lazily instantiating each value as []

    def add_constraint(self, constraint: ConstraintBase) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise ValueError(f"Variable: {variable} not in constraint satisfaction problem.")
            self.constraints[variable].append(constraint)
    
    def is_consistent(self, variable, assignment: dict) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.is_satisfied(assignment):
                return False
        return True
    
    def backtracking_search(self):
        pass

