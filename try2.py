from typing import List
import numpy as np

class Graph:
    # nodes = None
    # connections = None

    def __init__(self):
        self.connections = []
        self.nodes = []

    def getConnections(self, node):
        return [c for c in self.connections if c.getFromNode == node]


class Node:
    def __init__(self, number, status, costSoFar, estH, estT, previous, x, y):
        self.nodeNumber = number
        self.status = status
        self.costSoFar = costSoFar
        self.estimatedHeuristic = estH
        self.estimatedTotal = estT
        self.previousNode = previous
        self.x = x
        self.y = y

    def toString(self):
        return "Node Number " + str(self.nodeNumber) + ": Positioned at X = " + str(
            self.x) + " and Z = " + str(self.y)

    def __hash__(self):
        return hash((self.x, self.y))

class Connection:
    def __init__(self, number, fromNode, toNode, cost):
        self.connectionNumber = number
        self.fromNode = fromNode
        self.toNode = toNode
        self.cost = cost

    def toString(self):
        return "Connection Number " + str(self.connectionNumber) + ": Goes from Node " + str(
            self.fromNode) + " to Node " + str(self.toNode) + " and costs " + str(self.cost)
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


def pathfindAStar(graph, start: Node, goal: Node):
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
                endNodeHeuristic = heuristic(start, endNode)

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
    connections = {}
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.strip().split(', ')
            number = int(fields[1])
            from_node = int(fields[2])
            to_node = int(fields[3])
            cost = int(fields[4])
            plot_position = int(fields[5])
            connection_type = int(fields[6])

            if from_node not in connections:
                connections[from_node] = {}
            connections[from_node][to_node] = {
                'connection_type': connection_type,
                'number': number,
                'cost': cost,
                'plot_position': plot_position
            }

    return connections



def main():
    graph = Graph()
    # graph.nodes = read_nodes_file('CS 330, Pathfinding, Graph AB Nodes v3.txt')
    # graph.connections = read_connections('CS 330, Pathfinding, Graph AB Connections v3.txt')
    with open('CS 330, Pathfinding, Graph AB Connections v3.txt', 'r') as fin:  # cn, fn, tn, cc
        lines = fin.readlines()
        for i in lines:
            if "#" not in i:
                vals = i.split(",")
                for x in vals:
                    x.strip()
                cn = int(vals[1])
                fn = int(vals[2])
                tn = int(vals[3])
                cc = int(vals[4])
                graph.connections.append(Connection(cn, fn, tn, cc))
        fin.close()
    with open('CS 330, Pathfinding, Graph AB Nodes v3.txt', 'r') as f:
        lines = f.readlines()
        for i in lines:
            if '#' not in i:
                vals = i.split(',')
                for x in vals:
                    x.strip()
                nodeNum = int(vals[1])
                status = int(vals[2])
                csf = int(vals[3])
                estH = int(vals[4])
                estT = int(vals[5])
                prevNode = int(vals[6])
                x = float(vals[7])
                y = float(vals[8])
                graph.nodes.append(Node(nodeNum, status, csf, estH, estT, prevNode, x, y))
        f.close()
    start_node = graph.nodes[1]  # Replace 1 with the index of the desired start node
    goal_node = graph.nodes[29]  # Replace 29 with the index of the desired goal node
    path = pathfindAStar(graph, start_node, goal_node)
    print(path)


if __name__ == '__main__':
    main()
