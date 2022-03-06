import os
import unittest

from backtracking import backtracking_search
from graphcoloring import GraphColoringCSP
from fileparser import FileParser
from heuristics import lcv, mrv, static_ordering, unordered_domain_values
from inference import ac3, forward_checking, maintain_arc_consistency, no_inference, revise

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


class TestInference(unittest.TestCase):
    """Test cases for inference methods: forward checking, maintaining arc consistency with ac3"""
    def test_forward_checking(self):
        """
        Unit test for forward checking. We continue using the Australia problem, with the forward
        checking example given in Figure 6.7 of the Artificial Intelligence textbook.
        Territories are donoted as 0: WA, 1: NT, 2: SA, 3: Q, 4: NSW, 5: V, 6: T
        Colors are donoted by 0: 'red', 1: 'green', 2: 'blue'
        """
        csp = GraphColoringCSP.from_file(os.path.join("assets", "input_files", "australia.txt"))
        assignment = {}

        # WA=red
        variable = 0
        value = 0
        csp.assign(variable, value, assignment)
        csp.add_assignment(variable, value)
        inferences = forward_checking(csp, variable=variable, assignment=assignment)
        self.assertNotEqual(inferences, "failure")
        csp.add_inferences(inferences)
        # After this assignment, domains should be {0: [0], 1: [1, 2], 2: [1, 2], 3: [0, 1, 2], 4: [0, 1, 2], 5: [0, 1, 2], 6: [0, 1, 2]}
        expected_domains = {0: [0], 1: [1, 2], 2: [1, 2], 3: [0, 1, 2], 4: [0, 1, 2], 5: [0, 1, 2], 6: [0, 1, 2]}
        self.assertEqual(csp.current_domains, expected_domains, "Unexpected domain values in forward checking")

        # Q=green
        variable = 3
        value = 1
        csp.assign(variable, value, assignment)
        csp.add_assignment(variable, value)
        inferences = forward_checking(csp, variable=variable, assignment=assignment)
        self.assertNotEqual(inferences, "failure")
        csp.add_inferences(inferences)
        # After this assignment, domains should be {0: [0], 1: [2], 2: [2], 3: [1], 4: [0, 2], 5: [0, 1, 2], 6: [0, 1, 2]}
        expected_domains = {0: [0], 1: [2], 2: [2], 3: [1], 4: [0, 2], 5: [0, 1, 2], 6: [0, 1, 2]}
        self.assertEqual(csp.current_domains, expected_domains, "Unexpected domain values in forward checking")
        
        # V=blue
        variable = 5
        value = 2
        csp.assign(variable, value, assignment)
        csp.add_assignment(variable, value)
        inferences = forward_checking(csp, variable=variable, assignment=assignment)
        # After this assignment, the solution is inconsistent and domains would be {0: [0], 1: [2], 2: [], 3: [1], 4: [0], 5: [2], 6: [0, 1]}
        # The forward checking function should return 'failure'
        self.assertEqual(inferences, "failure")

    # def test_revise(self):
    #     """
    #     Unit test for the revise function. We want to ensure that this function doesn't revise if no conflicts
    #     exist, but does revise the domain if it encounters a conflict.
    #     """
    #     csp = GraphColoringCSP.from_file(os.path.join("assets", "input_files", "australia.txt"))
    #     assignment = {}
    #     variable = 0
    #     value = 0
    #     csp.assign(variable, value, assignment)
    #     csp.add_assignment(variable, value)
    #     # Once we've assigned {0: 0}, which has neighbors 1 and 2, we expect the domains for 1 and 2 to not have 0 in them
    #     expected_domains = {0: [0], 1: [1, 2], 2: [1, 2], 3: [0, 1, 2], 4: [0, 1, 2], 5: [0, 1, 2], 6: [0, 1, 2]}
    #     # Loop through the neighbors to revise as needed
    #     queue = [(x, variable) for x in csp.neighbors[variable]]
    #     for Xi, Xj in queue:
    #         revised = revise(csp, Xi, Xj)
    #     self.assertEqual(csp.current_domains, expected_domains)


    # def test_ac3(self):
    #     """
    #     Unit test for ac3 inference. This is tested very similarly to the revise algorithm
    #     """
    #     csp = GraphColoringCSP.from_file(os.path.join("assets", "input_files", "australia.txt"))
    #     assignment = {}
    #     variable = 0
    #     value = 0
    #     csp.assign(variable, value, assignment)
    #     csp.add_assignment(variable, value)
    #     # Once we've assigned {0: 0}, which has neighbors 1 and 2, we expect the domains for 1 and 2 to not have 0 in them
    #     expected_domains = {0: [0], 1: [1, 2], 2: [1, 2], 3: [0, 1, 2], 4: [0, 1, 2], 5: [0, 1, 2], 6: [0, 1, 2]}
    #     queue = [(x, variable) for x in csp.neighbors[variable]]
    #     inferences = ac3(csp, queue)
    #     self.assertEqual(csp.current_domains, expected_domains)
    
    # def test_maintain_arc_consistency(self):
    #     """
    #     Unit test for maintain arc consistency inference.
    #     """
    #     csp = GraphColoringCSP.from_file(os.path.join("assets", "input_files", "australia.txt"))
    #     assignment = {}
    #     variable = 0
    #     value = 0
    #     csp.assign(variable, value, assignment)
    #     csp.add_assignment(variable, value)
    #     inferences = maintain_arc_consistency(csp, variable, assignment)
    #     expected_domains = {0: [0], 1: [1, 2], 2: [1, 2], 3: [0, 1, 2], 4: [0, 1, 2], 5: [0, 1, 2], 6: [0, 1, 2]}
    #     self.assertEqual(csp.current_domains, expected_domains)


    
class TestBacktracking(unittest.TestCase):
    """
    Unit tests for backtracking search. These tests are executed on the test files (more than just the Australia example)
    """

    def test_backtracking_search_no_inference(self):
        """
        Unit test for backtracking search with no inference
        """
        folder = os.path.join("assets", "input_files")
        files = [file for file in os.listdir(folder) if not 'gc_1377121623225900' in file]
        no_solution = "gc_78317097930401.txt"
        for ix, file in enumerate(files):
            filepath = os.path.join(folder, file)
            csp = GraphColoringCSP.from_file(filepath)
            solution = backtracking_search(csp, verbose=False, 
                # select_unassigned_variable=static_ordering,
                # order_domain_values=unordered_domain_values,
                inference=no_inference
            )
            if file == no_solution:
                self.assertIsNone(solution)
            if solution:
                self.assertTrue(csp.valid_solution(solution))

    def test_backtracking_search_forward_checking(self):
        """
        Unit test for backtracking search with forward checking
        """
        folder = os.path.join("assets", "input_files")
        files = [file for file in os.listdir(folder) if not 'gc_1377121623225900' in file]
        no_solution = "gc_78317097930401.txt"
        for ix, file in enumerate(files):
            filepath = os.path.join(folder, file)
            csp = GraphColoringCSP.from_file(filepath)
            solution = backtracking_search(csp, verbose=False, inference=forward_checking)
            if file == no_solution:
                self.assertIsNone(solution)
            if solution:
                self.assertTrue(csp.valid_solution(solution))
            else:
                print(file)
    
#     def test_backtracking_search_mac(self):
#         """
#         Unit test for backtracking search with maintaining arc consistency using ac3
#         """
#         folder = os.path.join("assets", "input_files")
#         files = [file for file in os.listdir(folder) if not 'gc_1377121623225900' in file]
#         # filepath = os.path.join(folder, "australia.txt")
#         # csp = csp = GraphColoringCSP.from_file(filepath)
#         # solution = backtracking_search(csp, verbose=False)
#         # self.assertIsNotNone(solution, "Search returned no solution, although solution exists")
#         no_solution = "gc_78317097930401.txt"
#         solutions = []
#         for ix, file in enumerate(files):
#             filepath = os.path.join(folder, file)
#             csp = GraphColoringCSP.from_file(filepath)
#             # print(f"File {ix}")
#             solution = backtracking_search(csp, verbose=False, inference=maintain_arc_consistency)
#             solutions.append(solution)
#             # if not solution:
#             #     print(file)
#             if solution and not csp.valid_solution(solution):
#                 print("INVALID")
#             # if file == no_solution:
#             #     self.assertIsNone(solution, f"Search returned solution for file {file}, although no solution exists")
#             # else:
#             #     self.assertIsNotNone(solution, f"Search returned no solution for file {file}, although a solution exists")

if __name__ == "__main__":
    unittest.main()