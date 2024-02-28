import os
from ortools.linear_solver import pywraplp

# Initialize data structures
network_nodes = []
network_arcs = {}
od_pairs = {}
max_range = 100
distances = {}
paths = {}

def find_path(start, end):
    """Find a path from start to end."""
    current_node = start
    nodes = [current_node]
    path = []
    while current_node != end:
        for arc in network_arcs:
            if arc[0] == current_node:
                current_node = arc[1]
                nodes.append(current_node)
                path.append(arc)
                break
    return [nodes, path]

def setup_data_model():
    """Setup the data model."""
    # Read network nodes
    for filename in os.listdir('roads'):
        if filename.endswith("data/trafik.csv"):
            with open(os.path.join('roads', filename)) as f:
                lines = f.readlines()
                for line in  lines[1:]:
                    kkno, dilimno, length, vehicle, speed, start, end, connection = line.split(",")
                    if start not in network_nodes:
                        network_nodes.append(start)
                    if end not in network_nodes:
                        network_nodes.append(end)
                    start_index = network_nodes.index(start)
                    end_index = network_nodes.index(end)
                    network_arcs[(start_index, end_index)] = {
                        "kkno": kkno,
                        "dilimno": dilimno,
                        "length": length,
                        "vehicle": vehicle,
                        "speed": speed
                    }

    # Read cities
    cities = []
    with open(os.path.join('roads', 'data/cities.csv')) as f:
        lines = f.readlines()
        for line in lines:
            cities.append(line.strip())

    # Find paths between cities
    for i in range(0, len(cities)):
        for j in range(i, len(cities)):
            nodes, arches = find_path(network_nodes.index(cities[i]), network_nodes.index(cities[j]))
            if len(nodes) != 0:
                distance = calculate_distance(network_nodes.index(cities[i]), network_nodes.index(cities[j]))
                if distance > max_range:
                    od_pairs[(network_nodes.index(cities[i]), network_nodes.index(cities[j]))] = {"nodes": nodes, "arches": arches, "distance": distance}

def calculate_distance(i, j):
    """Calculate distance between two nodes."""
    if i > j:
        i, j = j, i
    if (i, j) in distances:
        return distances[(i, j)]
    curr = i
    distance = 0 
    while curr != j:
        if (curr, curr + 1) in network_arcs:
            distance += int(network_arcs[(curr, curr + 1)]["length"])
            curr = curr + 1
    distances[(i, j)] = distance
    return distance

def main():
    """Main function."""
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SAT")
    if not solver:
        return

    # Setup data model
    setup_data_model()

    # Print some statistics
    print("Number of network_nodes =", len(network_nodes))
    print("Number of arcs =", len(network_arcs))
    print("Number of od pairs =", len(od_pairs))

    # Create a binary decision variable y[i] for each refueling station.
    y = {}
    for i in range(0, len(network_nodes)):
        y[i] = solver.IntVar(0, 1, "y[%i]" % i)

    # Create decision variables and constraints for each OD pair
    x = {}
    for od_pair in od_pairs:
        expanded_arcs = []
        for node in od_pairs[od_pair]["nodes"]:
            if calculate_distance(od_pair[0], node) <= max_range / 2:
                expanded_arcs.append(("s", node))
        for node in od_pairs[od_pair]["nodes"]:
            if calculate_distance(od_pair[1], node) <= max_range / 2:
                expanded_arcs.append((node, "t"))
        for i in range(0, len(od_pairs[od_pair]["nodes"])):
            for j in range(i + 2, len(od_pairs[od_pair]["nodes"])):
                if calculate_distance(od_pairs[od_pair]["nodes"][i], od_pairs[od_pair]["nodes"][j]) <= max_range:
                    expanded_arcs.append((od_pairs[od_pair]["nodes"][i], od_pairs[od_pair]["nodes"][j]))
        od_pairs[od_pair]["expanded_arcs"] = od_pairs[od_pair]["arches"] + expanded_arcs
        x[od_pair] = {}
        for arc in od_pairs[od_pair]["expanded_arcs"]:
            x[od_pair][arc[0], arc[1]] = solver.IntVar(0, 1, "x(%i, %i)[%s,%s]" % (od_pair[0], od_pair[1], arc[0], arc[1]))
        for node in od_pairs[od_pair]["nodes"] + ["s", "t"]:
            right = 1 if node == "s" else -1 if node == "t" else 0
            solver.Add(sum(x[od_pair][node, arc[1]] for arc in od_pairs[od_pair]["expanded_arcs"] if arc[0] == node) - sum(x[od_pair][arc[0], node] for arc in od_pairs[od_pair]["expanded_arcs"] if arc[1] == node) == right)
        for i in range(0, len(network_nodes)):
            solver.Add(sum(x[od_pair][arc[0], i] for arc in od_pairs[od_pair]["expanded_arcs"] if arc[1] == i) <= y[i])

    # Objective function: minimize the number of refueling stations
    solver.Minimize(sum(y[i] for i in range(0, len(network_nodes))))

    # Model complete.
    print("Model complete")

    # Solve
    solver.Solve()

    # Print some statistics
    print("Number of constraints =", solver.NumConstraints())
    print("Number of variables =", solver.NumVariables())

    # Print solution
    number_of_stations = 0
    for i in range(0, len(network_nodes)):
        if y[i].solution_value() == 1:
            print(network_nodes[i])
            number_of_stations += 1
    print("Number of stations =", number_of_stations)

if __name__ == "__main__":
    main()