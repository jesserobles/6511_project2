import os
import unittest

from graphcoloring import GraphColoringCSP
from fileparser import FileParser
from heuristics import lcv, mrv
from inference import forward_checking

class TestFileParser(unittest.TestCase):

    def test_file_parser(self):
        """
        Unit test for parsing an input file and comparing the output
        with a known result.
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
        assignment = {
            0: 0, # WA=red
            1: 1 # NT=green
        }
        csp = GraphColoringCSP.from_file(os.path.join("assets", "input_files", "australia.txt"))
        csp.add_assignments(assignment)
        # WA=red, NT=green, now we try assigning SA=0, which should yield 1 conflict
        conflicts = csp.count_conflicts(2, 0, assignment)
        self.assertEqual(conflicts, 1, f"Expected 1 conflict, got {conflicts}")


class TestHeuristics(unittest.TestCase):
    def test_lcv(self):
        """
        Unit test for least constraining value. We'll use the explanation from the textbook
        as an example for this unittest:
        For example, suppose that for the Australia problem, we have generated 
        the partial assignment with WA(0)=red(0) and NT(1)=green(1) and that our next choice
        is for Q(3). The least-constraining value heuristic therefore prefers red(0) to blue(2).
        """
        assignment = {
            0: 0, # WA=red
            1: 1 # NT=green
        }
        csp = GraphColoringCSP.from_file(os.path.join("assets", "input_files", "australia.txt"))
        csp.add_assignments(assignment)
        self.assertEqual(lcv(csp, 3, assignment)[0], 0, "Should be 0")
    
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
    
    def test_forward_checking(self):
        """
        Unit test for forward checking. We continue using the Australia problem, with the forward
        checking example given in Figure 6.7 of the Artificial Intelligence textbook.
        Territories are donoted as 0: WA, 1: NT, 2: SA, 3: Q, 4: NSW, 5: V, 6: T
        Colors are donoted by 0: 'red', 1: 'green', 2: 'blue'
        """
        assignment = {}
        csp = GraphColoringCSP.from_file(os.path.join("assets", "input_files", "australia.txt"))
        consistent = forward_checking(csp, 0, 0, assignment) # WA=red
        self.assertTrue(consistent)
        # After this assignment, domains should be {0: [0], 1: [1, 2], 2: [1, 2], 3: [0, 1, 2], 4: [0, 1, 2], 5: [0, 1, 2], 6: [0, 1, 2]}
        expected_domains = {0: [0], 1: [1, 2], 2: [1, 2], 3: [0, 1, 2], 4: [0, 1, 2], 5: [0, 1, 2], 6: [0, 1, 2]}
        self.assertEqual(csp.current_domains, expected_domains, "Unexpected domain values in forward checking")

        consistent = forward_checking(csp, 3, 1, assignment) # Q=green
        self.assertTrue(consistent)
        # After this assignment, domains should be {0: [0], 1: [2], 2: [2], 3: [1], 4: [0, 2], 5: [0, 1, 2], 6: [0, 1, 2]}
        expected_domains = {0: [0], 1: [2], 2: [2], 3: [1], 4: [0, 2], 5: [0, 1, 2], 6: [0, 1, 2]}
        self.assertEqual(csp.current_domains, expected_domains, "Unexpected domain values in forward checking")

        consistent = forward_checking(csp, 5, 2, assignment) # V=blue
        # After this assignment, the solution is inconsisten, and domains should be {0: [0], 1: [2], 2: [], 3: [1], 4: [0], 5: [2], 6: [0, 1]}
        self.assertFalse(consistent)
        expected_domains = {0: [0], 1: [2], 2: [], 3: [1], 4: [0], 5: [2], 6: [0, 1]}
        self.assertEqual(csp.current_domains, expected_domains, "Unexpected domain values in forward checking")



class TestInference(unittest.TestCase):
    def test_forward_checking(self):
        pass

    def test_maintain_arc_consistency(self):
        pass
    

if __name__ == "__main__":
    unittest.main()