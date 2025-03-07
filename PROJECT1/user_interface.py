import time
import tracemalloc
import graph_setup
import search_algorithms

def main():
    """
    Revised main loop that:
      1) Loads data once
      2) Repeatedly asks for Start/Goal
      3) Lets user pick multiple search methods for the same Start/Goal
      4) Then asks if user wants a NEW Start/Goal or to quit
    """

    # --- Load city data once at startup ---
    coordinates = graph_setup.load_coordinates("coordinates.csv")
    graph = graph_setup.load_adjacencies("Adjacencies.txt")

    while True:
        # --- Ask user for start & goal one time ---
        cities = list(graph.keys())
        print("Available cities:", ", ".join(cities))

        start = input("Enter the starting city: ")
        while start not in cities:
            print("Invalid city. Try again.")
            start = input("Enter the starting city: ")

        goal = input("Enter the goal city: ")
        while goal not in cities:
            print("Invalid city. Try again.")
            goal = input("Enter the goal city: ")

        # --- Let user pick multiple methods for the same route ---
        while True:
            print("\nChoose a search method:")
            print("1. Breadth-First Search (BFS)")
            print("2. Depth-First Search (DFS)")
            print("3. Iterative Deepening DFS (ID-DFS)")
            print("4. Best-First Search")
            print("5. A* Search")

            choice = input("Enter the number of your chosen method: ")
            while choice not in ["1", "2", "3", "4", "5"]:
                print("Invalid choice. Try again.")
                choice = input("Enter the number of your chosen method: ")

            # Decide which search function to call
            if choice == "1":
                method_name = "BFS"
                search_fn = search_algorithms.bfs
            elif choice == "2":
                method_name = "DFS"
                search_fn = search_algorithms.dfs
            elif choice == "3":
                method_name = "ID-DFS"
                def search_fn(g, s, d, max_time=5.0):
                    return search_algorithms.id_dfs(g, s, d, max_depth=10, max_time=max_time)
            elif choice == "4":
                method_name = "Best-First Search"
                search_fn = search_algorithms.best_first_search
            else:
                method_name = "A* Search"
                search_fn = search_algorithms.a_star_search

            # Perform the search
            display_results(start, goal, method_name, search_fn, graph, coordinates)

            # Ask if user wants to pick another method for this same Start/Goal
            another = input("\nTry another method on the same route? (y/n): ").strip().lower()
            if another != "y":
                break

        # After finishing comparisons for this Start/Goal, ask if they want to do a new route
        again = input("\nDo you want to try a NEW start/goal route? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break


def display_results(start, goal, method_name, search_method, graph, coordinates):
    """
    Run the chosen search method, print path/time/memory/distance.
    """

    print(f"\nRunning {method_name} from {start} to {goal}...")

    tracemalloc.start()
    start_time = time.perf_counter()

    # Distinguish whether we pass coordinates or not
    if search_method in [search_algorithms.best_first_search, search_algorithms.a_star_search]:
        path, cost = search_method(graph, start, goal, coordinates, max_time=5.0)
    else:
        path, cost = search_method(graph, start, goal, max_time=5.0)

    end_time = time.perf_counter()
    memory_used = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()

    if path is not None:
        print("Path found:", " -> ".join(path))

        # Calculate real distance from consecutive city pairs
        total_distance = 0.0
        for i in range(len(path) - 1):
            city_a = path[i]
            city_b = path[i + 1]
            total_distance += graph_setup.haversine_distance(city_a, city_b, coordinates)

        print(f"Total distance: {total_distance:.2f} km")

        elapsed_seconds = end_time - start_time
        elapsed_ms = elapsed_seconds * 1000
        print(f"Time taken: {elapsed_seconds:.6f} s ({elapsed_ms:.3f} ms)")
        print(f"Memory used: {memory_used:.2f} KB")
    else:
        print("No path found.")
