import os
import unittest

from graphcoloring import GraphColoringCSP
from fileparser import FileParser
from heuristics import lcv, mrv

class TestFileParser(unittest.TestCase):

    def test_file_parser(self):
        """
        Unit test for parsing an input file and comparing the output
        with a known expected result.
        """
        expected_colors = 4
        expected_edges = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), 
            (2, 4), (2, 6), (2, 7), (3, 5), (3, 6), (3, 7), (4, 5),
            (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)]
        filepath = os.path.join("assets", "input_files", "gc_1378296846561000.txt")
        file_parser = FileParser(filepath)
        parsed_payload = file_parser.parsed_payload
        # Test colors
        colors = parsed_payload["colors"]
        self.assertEqual(colors, expected_colors, "Unexpected colors: {colors}")
        # Test edges: length of edges
        edges = parsed_payload["edges"]
        self.assertEqual(len(edges), len(expected_edges), f"Unexpected edge length: {len(edges)}")
        # Test edges: test each edge is in expected edges
        for edge in edges:
            self.assertIn(edge, expected_edges, f"Unexpected edge: {edge}")

class TestGraphColoringCSP(unittest.TestCase):
    """
    Test cases for the GraphColoringCSP class.
    """
    def test_count_conflicts(self):
        pass

class TestHeuristics(unittest.TestCase):
    def test_lcv(self):
        """
        Unit test for least constraining value
        """
    
    def test_mrv(self):
        """
        Unit test for minimum remaining values with tie breaking.
        We will use the Australia problem. This should return 2
        (South Australia), since the tie breaker should pick the
        variable involved in more constraints.
        """
        filepath = os.path.join("assets", "input_files", "australia.txt")
        csp = GraphColoringCSP.from_file(filepath)
        assignment = {}
        # assignment = {0: 0, 1: 1}
        variable = mrv(csp, assignment)
        self.assertEqual(variable, 2, f"MRV heuristic failed: expected 2, got {variable}")
        
        

if __name__ == "__main__":
    unittest.main()