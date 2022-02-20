from typing import Generic, List
from abc import ABC, abstractmethod


class Constraint:
    """Base class for constraints"""
    def __init__(self, variables: List) -> None:
        pass

    @abstractmethod
    def satisfied(self, assignment: List)->bool:
        pass


class ConstrainedSatisfactionProblem:
    """Base class for constrained satisfaction problems"""
    def __init__(self) -> None:
        pass