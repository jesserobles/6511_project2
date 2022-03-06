from collections import defaultdict
from typing import List, Set, Tuple, Union

from fileparser import FileParser

class GraphColoringConstraint:
    """
    Class representing the graph coloring constraint.
    The constraint for this problem is that neighbors cannot have the same color. Objects
    of this class are used in `GraphColoringCSP` objects to check whether constraints are 
    satisfied when checking a state's consitency in the `GraphColoringCSP.is_consistent` method.

    arguments:
        :vertex1: - One side of an edge
        :vertex2: - The other side of an edge
    """
    def __init__(self, vertex1, vertex2) -> None:
        self.variables = [vertex1, vertex2]
        self.vertex1 = vertex1
        self.vertex2 = vertex2
    
    def __repr__(self) -> str:
        return f"<Constraint: [vertex1: {self.vertex1}, vertex2: {self.vertex2}]>"
    
    def is_satisfied(self, assignment: dict) -> bool:
        """
        Returns whether neighbors A, B satisfy the constraint when they have values A=a, B=b.
        arguments:
            :assignment: - a dictionary with format {0:1, 1:1} where the keys are adjacent vertices and the
                values are their respectively assigned color. In this problem, the values should not be the same.
        """
        # If either vertex is unassigned, return True
        if self.vertex1 not in assignment or self.vertex2 not in assignment:
            return True
        # Otherwise return whether the vertices are the same color
        return assignment[self.vertex1] != assignment[self.vertex2]


class GraphColoringCSP:
    """
    Class representing the graph coloring problem. For this problem, we have
    X (variables) {X1, ..., Xn} are the vertices in the graph.
    D (domains) {D1, ..., Dn} are the possible colors for each variable, initially all colors.
    C (constraints) <(Xi, Xj), ci != cj>, where ci and cj are the colors assigned to adjacent vertices Xi and Xj.

    arguments:
        :edges: - A list or set of tuples where each tuple represents an edge between two vertices (e.g., (0, 1) represents an edge between vertices 0 and 1)
        :colors: - An integer representing the number of colors for the CSP problem. This gets converted to a list of values and added to the domains
        :neighbors: - A dictionary representing an adjacency list. The keys are a vertex, and the values are all of that vertex's neighbors.
    """
    def __init__(self, edges: Union[List[Tuple[int, int]], Set[Tuple[int, int]]], colors: int, neighbors:dict=None) -> None:
        self.neighbors = neighbors
        self.edges = edges
        self.neighbors = neighbors
        self.constraints: dict = defaultdict(list) # Equivalent to lazily instantiating each value as []
        self.colors = colors
        self.variables = set(vertex for edge in edges for vertex in edge)
        self.domains = {vertex: list(range(colors)) for vertex in self.variables}
        self.assignment_counts = 0
        # Now add constraints
        for vertex1, vertex2 in self.edges:
            self.add_constraint(GraphColoringConstraint(vertex1, vertex2))
    
    def constraint_function(self, X, x, Y, y):
        """
        Our constraint for this problem: neighbors X and Y cannot have the same value.
        """
        return x != y
    
    def add_constraint(self, constraint) -> None:
        """
        Method to add constraints, represented by the GraphColoringConstraint class, to our problem
        arguments:
            :constraint: - A constraint represented as a `GraphColoringConstraint` object
        """
        for variable in constraint.variables:
            if variable not in self.variables:
                raise ValueError(f"Variable: {variable} not in constraint satisfaction problem.")
            self.constraints[variable].append(constraint)
    
    def is_consistent(self, variable, assignment: dict) -> bool:
        """
        Method to determine of an assignment is consistent with all of the constraints.
        arguments:
            :variable: - whatever the vertex represents (i.e., state in map coloring)
            :assignment: - a dictionary with format {variable: value, ...}, e.g., {0: 1} where 0 is a vertex
                and 1 is the color for a graph coloring problem. So if we assign {0:1}, we want to check if
                there are any constraints on `variable` that are not satisfied.
        """
        for constraint in self.constraints[variable]:
            if not constraint.is_satisfied(assignment):
                return False
        return True

    def add_assignment(self, variable, value):
        """
        Method to update the domains attribute to account for var=value.
        Used in unit tests.
        """
        removals = [(variable, a) for a in self.domains[variable] if a != value]
        self.domains[variable] = [value]
        return removals
    
    def add_assignments(self, assignments):
        """
        Method to update the domains attribute based on an assignment.
        Used in unit tests.
        """
        removals = []
        for variable, value in assignments.items():
            removals.append(self.add_assignment(variable, value))
        return removals

    def assign(self, variable, value, assignment):
        """
        Method that adds variable=value to assignment and updates the assignment count.
        """
        assignment[variable] = value
        self.assignment_counts += 1
    
    def add_inferences(self, inferences):
        """
        Method to add inferences to the CSP during backtracking. This updates the domains attribute.
        """
        for variable, values in inferences.items():
            for value in values:
                self.domains[variable].remove(value)

    def remove_inferences(self, inferences):
        """
        Method to restore removed values from the domain back into the domains attribute.
        """
        for variable, values in inferences.items():
            for value in values:
                self.domains[variable].append(value)

    def count_conflicts(self, var, val, assignment):
        """
        Method that returns the number of conflicts var=val has with other variables already assigned (in assignment)
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
        """
        Method to check if an assignment is a complete and valid solution. 
        The goal is to assign all variables, with all constraints satisfied.
        """
        if not assignment:
            return False
        return (len(assignment) == len(self.variables)
                and all(self.count_conflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    @classmethod
    def from_file(cls, filepath):
        """
        Method to conveniently create a GraphColoringCSP object from an input file.
        """
        fileparse = FileParser(filepath=filepath)
        return cls(**fileparse.parsed_payload)
