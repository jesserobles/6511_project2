from collections import defaultdict


class FileParser:
    """
    A class to parse an input file representing a graph coloring CSP problem.
    The format of the input files have a line specifying the number of colors
    for the problem (e.g., `colors = 3`), and lines representing edges between
    adjacent vertices (e.g., `0,1`). Some of these might be repeated (e.g., 
    `0,1` and `1,0`) so this class accounts for that by first sorting each edge.

    arguments:
        :filepath: - A string of the relative path to the file.
    """
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.parsed_payload = self.parse_file()
    
    def parse_file(self) -> dict:
        """
        Method to parse a graph coloring problem input file
        Returns a dictionary with colors, neighbors, and edges.
        """
        neighbors = defaultdict(set)
        edges = []
        csp_payload = {}
        with open(self.filepath, "r") as file:
            for line in file:
                if not line.strip() or line.strip().startswith('#'):
                    # Skip empty lines and comments
                    continue
                if line.lower().strip().startswith('colors'):
                    # Color line
                    csp_payload["colors"] = int(line.split('=')[-1].strip())
                else:
                    # Edge line
                    edge = tuple(sorted(int(element.strip()) for element in line.strip().split(',')))
                    edges.append(edge)
                    neighbors[edge[0]].add(edge[1])
                    neighbors[edge[1]].add(edge[0])
        csp_payload["edges"] = edges
        csp_payload["neighbors"] = neighbors
        return csp_payload