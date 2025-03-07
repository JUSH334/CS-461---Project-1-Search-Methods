import unittest
import os
import tempfile
import math
import graph_setup


class TestGraphSetup(unittest.TestCase):

    def test_haversine_distance(self):
        coords = {
            "Wichita": (37.6872, -97.3301),
            "Topeka": (39.0558, -95.6894),
        }
        distance = graph_setup.haversine_distance("Wichita", "Topeka", coords)

        # Allows a ±20 km margin around 220 km:
        self.assertAlmostEqual(distance, 220.0, delta=20.0,
                               msg=f"Expected ~220km, but got {distance:.2f}km")

    def test_load_coordinates(self):
        """
        Test load_coordinates by creating a temporary CSV file.
        """
        csv_content = """CityName,Latitude,Longitude
TestCityA,37.0,-97.0
TestCityB,38.5,-96.2
"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            coords = graph_setup.load_coordinates(tmp_path)
            self.assertIn("TestCityA", coords)
            self.assertIn("TestCityB", coords)
            self.assertEqual(coords["TestCityA"], (37.0, -97.0))
            self.assertEqual(coords["TestCityB"], (38.5, -96.2))
        finally:
            os.remove(tmp_path)

    def test_load_adjacencies(self):
        """
        Test load_adjacencies by creating a temporary adjacency file.
        """
        txt_content = """CityA CityB
CityB CityC
"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp.write(txt_content)
            tmp_path = tmp.name

        try:
            graph = graph_setup.load_adjacencies(tmp_path)
            self.assertIn("CityA", graph)
            self.assertIn("CityB", graph)
            self.assertIn("CityC", graph)

            self.assertIn("CityB", graph["CityA"])
            self.assertIn("CityA", graph["CityB"])  # Because it's bidirectional
            self.assertIn("CityB", graph["CityC"])  # Because CityC CityB too
            self.assertIn("CityC", graph["CityB"])
        finally:
            os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
