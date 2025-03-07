import csv
import math

def load_coordinates(file_path):
    coordinates = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        # Comment out or remove the header skip line, because there's no header in your file
        # next(reader, None)
        for row in reader:
            city, lat, lon = row[0], float(row[1]), float(row[2])
            coordinates[city] = (lat, lon)
    return coordinates

def load_adjacencies(file_path):
    """
    Loads adjacency list from a text file and creates a graph dictionary.
    Each line has two city names separated by whitespace,
    e.g., "Anthony Bluff_City".
    """
    graph = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            city1, city2 = line.split()
            if city1 not in graph:
                graph[city1] = []
            if city2 not in graph:
                graph[city2] = []
            # Bidirectional connection
            graph[city1].append(city2)
            graph[city2].append(city1)
    return graph


def haversine_distance(city1, city2, coordinates):
    """
    Computes the great-circle distance between two cities (in km),
    using the Haversine formula on their lat/long from 'coordinates'.
    """
    if city1 not in coordinates or city2 not in coordinates:
        return float('inf')  # Return large value if city not found

    R = 6371.0  # Earth radius in km
    lat1, lon1 = coordinates[city1]
    lat2, lon2 = coordinates[city2]

    # Convert degrees to radians
    lat1, lon1 = math.radians(lat1), math.radians(lon1)
    lat2, lon2 = math.radians(lat2), math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
