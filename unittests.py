import os
import unittest

from fileparser import FileParser

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


if __name__ == "__main__":
    unittest.main()