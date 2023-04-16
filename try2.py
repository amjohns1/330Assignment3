from typing import List


class Graph:
    def __init__(self, connections):
        self.connections = connections

    def getConnections(self, node):
        return [c for c in self.connections if c.getFromNode == node]


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def is_goal(node, goal):
    return node == goal


def heuristic(node1, node2):
    return abs(node1.x - node2.x) + (node1.y - node2.y)
class NodeRecord:
    def __init__(self, node: Node, connection, costSoFar: float, estimatedTotalCost: float):
        self.node = node
        self.connection = connection
        self.costSoFar = costSoFar
        self.estimatedTotalCost = estimatedTotalCost


def pathfindAStar(graph: Graph, start: Node, goal: Node, heuristic):
    # Initialize the record for the start node.
    startRecord = NodeRecord(start, None, 0, heuristic(start, goal))

    # Initialize the open and closed lists.
    open = [startRecord]
    closed = []

    # Iterate through processing each node.
    while len(open) > 0:
        # Find the smallest element in the open list (using the estimatedTotalCost).
        current = min(open, key=lambda x: x.estimatedTotalCost)

        # If it is the goal node, then terminate.
        if current.node == goal:
            break

        # Otherwise get its outgoing connections.
        connections = graph.getConnections(current.node)

        # Loop through each connection in turn.
        for connection in connections:
            # Get the cost estimate for the end node.
            endNode = connection.getToNode()
            endNodeCost = current.costSoFar + connection.getCost()

            # If the node is closed we may have to skip, or remove it from the closed list.
            if endNode in [record.node for record in closed]:
                # Here we find the record in the closed list corresponding to the endNode.
                endNodeRecord = next((record for record in closed if record.node == endNode), None)

                # If we didn't find a shorter route, skip.
                if endNodeRecord.costSoFar <= endNodeCost:
                    continue

                # Otherwise remove it from the closed list.
                closed.remove(endNodeRecord)

                # We can use the node's old cost values to calculate its heuristic without calling the possibly expensive heuristic function.
                endNodeHeuristic = endNodeRecord.estimatedTotalCost - endNodeRecord.costSoFar

            # Skip if the node is open and we've not found a better route.
            elif endNode in [record.node for record in open]:
                # Here we find the record in the open list corresponding to the endNode.
                endNodeRecord = next((record for record in open if record.node == endNode), None)

                # If our route is no better, then skip.
                if endNodeRecord.costSoFar <= endNodeCost:
                    continue

                # Again, we can calculate its heuristic.
                endNodeHeuristic = endNodeRecord.estimatedTotalCost - endNodeRecord.costSoFar

            # Otherwise we know we've got an unvisited node, so make a record for it.
            else:
                endNodeRecord = NodeRecord(endNode, None, -1, -1)

                # We'll need to calculate the heuristic value using the function, since we don't have an existing record to use.
                endNodeHeuristic = heuristic.estimate(endNode)

            # We're here if we need to update the node. Update the cost, estimate and connection.
            endNodeRecord.costSoFar = endNodeCost
            endNodeRecord.connection = connection
            endNodeRecord.estimatedTotalCost = endNodeCost + endNodeHeuristic

            # And add it to the open list.
            if endNode not in [record.node for record in open]:
                open.append(endNodeRecord)
        open.remove(current)
        closed.append(current)
        if current.node != goal:
            return list()
        else:
            path = []
        while current.node != start:
            path.append(current.connection)
            current = current.connection.getFromNode()
        return list(reversed(path))

def read_nodes_file(filename):
        nodes = {}
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith("#"):
                    continue
                fields = line.strip().split(", ")
                node_number = int(fields[1])
                status = int(fields[2])
                cost_so_far = float(fields[3])
                estimated_heuristic = float(fields[4])
                estimated_total = float(fields[5])
                previous_node = int(fields[6]) if fields[6] else None
                x = float(fields[7])
                z = float(fields[8])
                number_plot_pos = int(fields[9])
                name_plot_pos = int(fields[10])
                node_name = fields[11]

                nodes[node_number] = {
                    'status': status,
                    'cost_so_far': cost_so_far,
                    'estimated_heuristic': estimated_heuristic,
                    'estimated_total': estimated_total,
                    'previous_node': previous_node,
                    'x': x,
                    'z': z,
                    'number_plot_pos': number_plot_pos,
                    'name_plot_pos': name_plot_pos,
                    'node_name': node_name
                }
        return nodes
def read_connections(filename):
    connections = []
    with open(filename, 'r') as f:
        for line in f:
            fields = line.strip().split(', ')
            connection = {
                'type': fields[0],
                'number': int(fields[1]),
                'from_node': int(fields[2]),
                'to_node': int(fields[3]),
                'cost': int(fields[4]),
                'plot_position': int(fields[5]),
                'connection_type': int(fields[6])
            }
            connections.append(connection)
    return connections

def main():
