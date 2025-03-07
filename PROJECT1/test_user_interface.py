import unittest
from unittest.mock import patch
import io
import user_interface

class TestUserInterfaceDeep(unittest.TestCase):

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input")
    def test_main_single_method_then_exit(self, mock_input, mock_stdout):
        """
        Scenario:
         1) Start = 'Anthony'
         2) Goal = 'Salina'
         3) Method = '1' (BFS)
         4) Another method? => 'n'
         5) New route? => 'n'
         => Program exits
        """
        mock_input.side_effect = [
            # Outer loop: pick start & goal
            "Anthony",
            "Salina",
            # Inner loop: pick BFS
            "1",
            # Another method with same route? => no
            "n",
            # Do we want a NEW start/goal? => no => exit
            "n"
        ]

        user_interface.main()
        output = mock_stdout.getvalue()

        self.assertIn("Running BFS from Anthony to Salina", output)
        self.assertIn("Path found:", output)
        self.assertIn("Total distance:", output)
        self.assertIn("Time taken:", output)
        self.assertIn("Memory used:", output)
        self.assertIn("Goodbye!", output)


    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input")
    def test_main_multiple_methods_same_route(self, mock_input, mock_stdout):
        """
        Scenario:
         1) Start = 'Anthony'
         2) Goal = 'Salina'
         3) Method = '1' (BFS)
         4) Another method? => 'y'
         5) Method = '2' (DFS)
         6) Another method? => 'n'
         7) New route? => 'n' => exit
        """
        mock_input.side_effect = [
            "Anthony",
            "Salina",
            "1",   # BFS
            "y",   # choose another method
            "2",   # DFS
            "n",   # no more methods
            "n"    # no new route
        ]

        user_interface.main()
        output = mock_stdout.getvalue()

        # BFS check
        self.assertIn("Running BFS from Anthony to Salina", output)
        self.assertIn("Path found:", output)

        # DFS check
        self.assertIn("Running DFS from Anthony to Salina", output)

        self.assertIn("Goodbye!", output)


    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input")
    def test_main_new_route_after_first(self, mock_input, mock_stdout):
        """
        Scenario:
         1) First route: A) Start=Anthony, B) Goal=Salina
         2) Method = '1' (BFS)
         3) Another method => 'n'
         4) New route => 'y'
         5) Next route: A) Start=Attica, B) Goal=Wichita
         6) Method = '5' (A* Search)
         7) Another method => 'n'
         8) New route => 'n' => exit
        """
        mock_input.side_effect = [
            # First route
            "Anthony",
            "Salina",
            "1",     # BFS
            "n",     # no more methods for first route
            # Start a new route
            "y",
            # Second route
            "Attica",
            "Wichita",
            "5",     # A* Search
            "n",     # no more methods for second route
            "n"      # no new route => exit
        ]

        user_interface.main()
        output = mock_stdout.getvalue()

        self.assertIn("Running BFS from Anthony to Salina", output)
        self.assertIn("Path found:", output)

        self.assertIn("Running A* Search from Attica to Wichita", output)
        self.assertIn("Path found:", output)

        self.assertIn("Goodbye!", output)


    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input")
    def test_main_invalid_city_then_correct(self, mock_input, mock_stdout):
        """
        Scenario:
         1) Enter invalid city => 'FooTown' (not in the city list)
         2) Then correct it => 'Anthony'
         3) Enter valid goal => 'Salina'
         4) Choose BFS => '1'
         5) Another method => 'n'
         6) New route => 'n' => exit
        """
        mock_input.side_effect = [
            "FooTown",  # invalid
            "Anthony",  # valid
            "Salina",
            "1",
            "n",
            "n"
        ]

        user_interface.main()
        output = mock_stdout.getvalue()

        self.assertIn("Invalid city. Try again.", output)
        self.assertIn("Running BFS from Anthony to Salina", output)
        self.assertIn("Path found:", output)
        self.assertIn("Goodbye!", output)


    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input")
    def test_main_invalid_method_then_correct(self, mock_input, mock_stdout):
        """
        Scenario:
         1) Start=Anthony
         2) Goal=Salina
         3) Enter method => '9' (invalid)
         4) Then correct it => '1' => BFS
         5) Another method => 'n'
         6) New route => 'n' => exit
        """
        mock_input.side_effect = [
            "Anthony",
            "Salina",
            "9",     # invalid choice
            "1",     # BFS
            "n",
            "n"
        ]

        user_interface.main()
        output = mock_stdout.getvalue()

        self.assertIn("Invalid choice. Try again.", output)
        self.assertIn("Running BFS from Anthony to Salina", output)
        self.assertIn("Path found:", output)
        self.assertIn("Goodbye!", output)

if __name__ == "__main__":
    unittest.main()
