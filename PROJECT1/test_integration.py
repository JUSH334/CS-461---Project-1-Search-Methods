import unittest
import graph_setup
import search_algorithms

class TestIntegrationWithRealData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Load the real adjacency and coordinate files once, for all tests.
        Adjust filenames if your CSV/TXT have different names or paths.
        """
        cls.coordinates = graph_setup.load_coordinates("coordinates.csv")
        cls.graph = graph_setup.load_adjacencies("Adjacencies.txt")

        # We'll use "Anthony" -> "Salina" for a route that *does* exist.
        # For no-route scenario, we'll do "Anthony" -> "Fake_City".
        cls.real_start = "Anthony"
        cls.real_goal = "Salina"
        cls.fake_goal = "Fake_City"

    # -------------------------------------------------------------------------
    # 1. BFS Tests
    # -------------------------------------------------------------------------
    def test_bfs_route_exists(self):
        path, cost = search_algorithms.bfs(self.graph, self.real_start, self.real_goal, max_time=5.0)
        self.assertIsNotNone(path, "BFS should find a route from Anthony to Salina in real data.")
        self.assertNotEqual(cost, float('inf'), "BFS cost shouldn't be inf for a valid route.")

        # For debugging: you can print the path
        print("BFS (Anthony -> Salina):", path)

    def test_bfs_route_not_exists(self):
        path, cost = search_algorithms.bfs(self.graph, self.real_start, self.fake_goal, max_time=5.0)
        self.assertIsNone(path, "BFS should not find a route to Fake_City.")
        self.assertEqual(cost, float('inf'), "Cost should be inf for nonexistent route.")

    # -------------------------------------------------------------------------
    # 2. DFS Tests
    # -------------------------------------------------------------------------
    def test_dfs_route_exists(self):
        path, cost = search_algorithms.dfs(self.graph, self.real_start, self.real_goal, max_time=5.0)
        self.assertIsNotNone(path, "DFS should find a route from Anthony to Salina.")
        self.assertNotEqual(cost, float('inf'))

        print("DFS (Anthony -> Salina):", path)

    def test_dfs_route_not_exists(self):
        path, cost = search_algorithms.dfs(self.graph, self.real_start, self.fake_goal, max_time=5.0)
        self.assertIsNone(path)
        self.assertEqual(cost, float('inf'))

    # -------------------------------------------------------------------------
    # 3. ID-DFS Tests
    # -------------------------------------------------------------------------
    def test_id_dfs_route_exists(self):
        path, cost = search_algorithms.id_dfs(self.graph, self.real_start, self.real_goal,
                                              max_depth=15, max_time=5.0)
        self.assertIsNotNone(path, "ID-DFS should find a route from Anthony to Salina.")
        self.assertNotEqual(cost, float('inf'))

        print("ID-DFS (Anthony -> Salina):", path)

    def test_id_dfs_route_not_exists(self):
        path, cost = search_algorithms.id_dfs(self.graph, self.real_start, self.fake_goal,
                                              max_depth=15, max_time=5.0)
        self.assertIsNone(path)
        self.assertEqual(cost, float('inf'))

    # -------------------------------------------------------------------------
    # 4. Best-First Search Tests
    # -------------------------------------------------------------------------
    def test_best_first_route_exists(self):
        path, cost = search_algorithms.best_first_search(
            self.graph, self.real_start, self.real_goal, self.coordinates, max_time=5.0
        )
        self.assertIsNotNone(path, "Best-First should find a route from Anthony to Salina.")
        self.assertNotEqual(cost, float('inf'))

        print("Best-First (Anthony -> Salina):", path)

    def test_best_first_route_not_exists(self):
        path, cost = search_algorithms.best_first_search(
            self.graph, self.real_start, self.fake_goal, self.coordinates, max_time=5.0
        )
        self.assertIsNone(path)
        self.assertEqual(cost, float('inf'))

    # -------------------------------------------------------------------------
    # 5. A* Search Tests
    # -------------------------------------------------------------------------
    def test_astar_route_exists(self):
        path, cost = search_algorithms.a_star_search(
            self.graph, self.real_start, self.real_goal, self.coordinates, max_time=5.0
        )
        self.assertIsNotNone(path, "A* should find a route from Anthony to Salina.")
        self.assertNotEqual(cost, float('inf'))

        print("A* (Anthony -> Salina):", path)

    def test_astar_route_not_exists(self):
        path, cost = search_algorithms.a_star_search(
            self.graph, self.real_start, self.fake_goal, self.coordinates, max_time=5.0
        )
        self.assertIsNone(path)
        self.assertEqual(cost, float('inf'))


if __name__ == "__main__":
    unittest.main()
