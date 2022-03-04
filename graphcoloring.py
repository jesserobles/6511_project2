from collections import deque
from typing import Dict, List, Set, Tuple, Union

from constraint import ConstraintBase, CSPBase
from fileparser import FileParser

class GraphColoringConstraint(ConstraintBase):
    """
    Subclass of CSPBase representing the graph coloring constraint satisfaction problem.
    For this problem:
        variables -> the vertices in the graph
        domains -> the colors represented by [0, colors)
    Assignments are of the format {2: 0}, where 2 is the vertex, and 0 is the color
        constraints -> assignment[v1] != assignment[v2]
    """
    def __init__(self, vertex1, vertex2) -> None:
        super().__init__([vertex1, vertex2])
        self.vertex1 = vertex1
        self.vertex2 = vertex2
    
    def is_satisfied(self, assignment: dict) -> bool:
        """
        Returns whether neighbors A, B satisfy the constraint when they have values A=a, B=b.

        assignment: a dictionary with format {0:1} where the key is the vertex and the
            value is the assigned color. In this problem, the values should not be the same.
        """
        # If either vertex is unassigned, return True
        if self.vertex1 not in assignment or self.vertex2 not in assignment:
            return True
        # Otherwise return whether the vertices are the same color
        return assignment[self.vertex1] != assignment[self.vertex2]


class GraphColoringCSP(CSPBase):
    """
    Sublcass of CSPBase representing the graph coloring problem. For this problem, we have
    X (variables) {X1, ..., Xn} are the vertices in the graph.
    D (domains) {D1, ..., Dn} are the possible colors for each variable, initially all colors.
    C (constraints) <(Xi, Xj), ci != cj>, where ci and cj are the colors assigned to adjacent vertices Xi and Xj.
    """
    def __init__(self, edges: Union[List[Tuple[int, int]], Set[Tuple[int, int]]], colors: int, neighbors:dict=None) -> None:
        self.edges = edges
        self.neighbors = neighbors
        # Maintain list of arcs on object to improve speed
        self.arcs = deque(set(list(self.edges) + [(v[-1], v[0]) for v in self.edges]))
        self.colors = colors
        vertices = set(vertex for edge in edges for vertex in edge)
        domains = {vertex: list(range(colors)) for vertex in vertices}
        super().__init__(vertices, domains, neighbors)
        # Now add constraints
        for vertex1, vertex2 in self.edges:
            self.add_constraint(GraphColoringConstraint(vertex1, vertex2))

    @classmethod
    def from_file(cls, filepath) -> CSPBase:
        fileparse = FileParser(filepath=filepath)
        return cls(**fileparse.parsed_payload)

if __name__ == "__main__":
    from time import time
    from datetime import datetime, timedelta
    
    start = time()
    gc = GraphColoringCSP.from_file('assets/input_files/gc_1377121623225900.txt')
    end = time()
    print(f"Finished parsing in {timedelta(seconds=end - start)}")
    start = time()
    assignment = gc.backtracking_search()
    end = time()
    print(f"Finished search in {timedelta(seconds=end - start)}")

