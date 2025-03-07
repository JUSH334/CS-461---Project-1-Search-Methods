import unittest
import graph_setup
import search_algorithms
import time

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

class TestSearchTimeout(unittest.TestCase):

    def setUp(self):
        # Define a larger graph (5000+ nodes) to force long execution time
        self.graph = {str(i): [str(i + 1)] for i in range(5000)}
        self.graph["4999"] = []  # The last node has no outgoing edges
        self.coords = {str(i): (37.0 + i * 0.01, -97.0) for i in range(5000)}  # Fake coordinates

    def test_bfs_timeout(self):
        """Ensure BFS times out correctly."""
        start_time = time.perf_counter()
        path, cost = search_algorithms.bfs(self.graph, "0", "4999", max_time=0.0001)
        elapsed_time = time.perf_counter() - start_time

        self.assertIsNone(path, "Expected BFS to time out.")
        self.assertEqual(cost, float('inf'), "Cost should be inf when BFS times out.")
        self.assertLessEqual(elapsed_time, 0.01, "BFS should have timed out quickly.")

    def test_dfs_timeout(self):
        """Ensure DFS times out correctly."""
        start_time = time.perf_counter()
        path, cost = search_algorithms.dfs(self.graph, "0", "4999", max_time=0.0001)
        elapsed_time = time.perf_counter() - start_time

        self.assertIsNone(path, "Expected DFS to time out.")
        self.assertEqual(cost, float('inf'), "Cost should be inf when DFS times out.")
        self.assertLessEqual(elapsed_time, 0.01, "DFS should have timed out quickly.")

    def test_id_dfs_timeout(self):
        """Ensure ID-DFS times out correctly."""
        start_time = time.perf_counter()
        path, cost = search_algorithms.id_dfs(self.graph, "0", "4999", max_depth=5000, max_time=0.0001)
        elapsed_time = time.perf_counter() - start_time

        self.assertIsNone(path, "Expected ID-DFS to time out.")
        self.assertEqual(cost, float('inf'), "Cost should be inf when ID-DFS times out.")
        self.assertLessEqual(elapsed_time, 0.01, "ID-DFS should have timed out quickly.")

    def test_best_first_search_timeout(self):
        """Ensure Best-First Search times out correctly."""
        start_time = time.perf_counter()
        path, cost = search_algorithms.best_first_search(self.graph, "0", "4999", self.coords, max_time=0.0001)
        elapsed_time = time.perf_counter() - start_time

        self.assertIsNone(path, "Expected Best-First Search to time out.")
        self.assertEqual(cost, float('inf'), "Cost should be inf when Best-First Search times out.")
        self.assertLessEqual(elapsed_time, 0.01, "Best-First Search should have timed out quickly.")

    def test_a_star_search_timeout(self):
        """Ensure A* Search times out correctly."""
        start_time = time.perf_counter()
        path, cost = search_algorithms.a_star_search(self.graph, "0", "4999", self.coords, max_time=0.0001)
        elapsed_time = time.perf_counter() - start_time

        self.assertIsNone(path, "Expected A* Search to time out.")
        self.assertEqual(cost, float('inf'), "Cost should be inf when A* Search times out.")
        self.assertLessEqual(elapsed_time, 0.01, "A* Search should have timed out quickly.")


if __name__ == "__main__":
    unittest.main()
