import unittest
import graph_setup
import search_algorithms

class TestSearchAlgorithms(unittest.TestCase):

    def setUp(self):
        """
        We'll define a small graph with a disconnected node "X".
        Graph shape:
            A -- B -- C
             \   |
              \  D -- E
            X  (no edges)

        So there's no path from A (or B/C/D/E) to X.
        """
        self.graph = {
            "A": ["B", "D"],
            "B": ["A", "C", "D"],
            "C": ["B"],
            "D": ["A", "B", "E"],
            "E": ["D"],
            "X": []  # Disconnected
        }
        # Contrived coordinates for each city, so that A->B->C is roughly in one line,
        # D is "down," E is further "down," and X is separate.
        self.coords = {
            "A": (37.0, -97.0),
            "B": (37.0, -96.5),
            "C": (37.0, -96.0),
            "D": (36.5, -96.5),
            "E": (36.0, -96.5),
            "X": (36.0, -98.0)  # Irrelevant for distance, but included
        }

    # ------------------------------------------------------------------------
    # SUCCESSFUL ROUTE TESTS (A route exists)
    # ------------------------------------------------------------------------
    def test_bfs(self):
        path, cost = search_algorithms.bfs(self.graph, "A", "C")
        # BFS -> shortest path in edges is A->B->C
        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(cost, 2)

    def test_dfs(self):
        path, cost = search_algorithms.dfs(self.graph, "A", "C")
        # DFS might find A->B->C directly or A->D->B->C, depending on stack order
        valid_paths = [
            ["A", "B", "C"],
            ["A", "D", "B", "C"]
        ]
        self.assertIn(path, valid_paths)

    def test_id_dfs(self):
        path, cost = search_algorithms.id_dfs(self.graph, "A", "E", max_depth=5)
        # Possible solutions: A->D->E or A->B->D->E
        valid_paths = [
            ["A", "D", "E"],
            ["A", "B", "D", "E"]
        ]
        self.assertIsNotNone(path, "Expected to find a path to E.")
        self.assertIn(path, valid_paths)

    def test_best_first_search(self):
        path, cost = search_algorithms.best_first_search(
            self.graph, "A", "C", self.coords
        )
        # Typically picks A->B->C due to the heuristic
        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(cost, 2)

    def test_a_star_search(self):
        path, dist_travelled = search_algorithms.a_star_search(
            self.graph, "A", "C", self.coords
        )
        # A->B->C is presumably the minimal-distance route
        self.assertEqual(path, ["A", "B", "C"])

        # Check actual distance is sum of A->B plus B->C
        ab = graph_setup.haversine_distance("A", "B", self.coords)
        bc = graph_setup.haversine_distance("B", "C", self.coords)
        expected = ab + bc
        self.assertAlmostEqual(dist_travelled, expected, delta=0.001)

    # ------------------------------------------------------------------------
    # NO ROUTE TESTS (A route does NOT exist)
    # ------------------------------------------------------------------------
    def test_bfs_no_route(self):
        path, cost = search_algorithms.bfs(self.graph, "A", "X")
        self.assertIsNone(path, "Expected no path to X.")
        self.assertEqual(cost, float('inf'), "Cost should be inf when no path is found.")

    def test_dfs_no_route(self):
        path, cost = search_algorithms.dfs(self.graph, "A", "X")
        self.assertIsNone(path)
        self.assertEqual(cost, float('inf'))

    def test_id_dfs_no_route(self):
        path, cost = search_algorithms.id_dfs(self.graph, "A", "X", max_depth=10)
        self.assertIsNone(path)
        self.assertEqual(cost, float('inf'))

    def test_best_first_search_no_route(self):
        path, cost = search_algorithms.best_first_search(
            self.graph, "A", "X", self.coords
        )
        self.assertIsNone(path)
        self.assertEqual(cost, float('inf'))

    def test_a_star_no_route(self):
        path, cost = search_algorithms.a_star_search(
            self.graph, "A", "X", self.coords
        )
        self.assertIsNone(path)
        self.assertEqual(cost, float('inf'))


if __name__ == "__main__":
    unittest.main()
