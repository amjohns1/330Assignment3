from typing import List
import numpy as np

"""
Class: CS 330
Authors: Adam Johnson & Erik Overberg
Program: Assignment 3
Implements A* Algorithm and outputs results to a file
"""


class Graph: #Holds all nodes and connections
    # nodes = None
    # connections = None

    def __init__(self):
        self.connections = []
        self.nodes = []

    def getConnections(self, node):
        return [c for c in self.connections if c.fromNode == node.nodeNumber]


class Node: #duh
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
            self.x) + " and Z = " + str(self.y) + '\n'

    def __hash__(self):
        return hash((self.x, self.y))


class Connection: #also duh
    def __init__(self, number, fromNode, toNode, cost):
        self.connectionNumber = number
        self.fromNode = fromNode
        self.toNode = toNode
        self.cost = cost

    def toString(self):
        return "Connection Number " + str(self.connectionNumber) + ": Goes from Node " + str(
            self.fromNode) + " to Node " + str(self.toNode) + " with cost " + str(self.cost) + '\n'


def is_goal(node, goal):
    return node == goal


def heuristic(node1, node2): #uses manhattan distance
    return abs(node1.x - node2.x) + (node1.y - node2.y)


def pathfindAStar(graph, start, goal):
    # This structure is used to keep track of the information we need for each node.
    class NodeRecord:
        def __init__(self, node, connection, costSoFar, estimatedTotalCost):
            self.node = node
            self.connection = connection
            self.costSoFar = costSoFar
            self.estimatedTotalCost = estimatedTotalCost

    # Initialize the record for the start node.
    startRecord = NodeRecord(start, None, 0, heuristic(start, goal))

    # Initialize the open and closed lists.
    openList = [startRecord]
    closedList = []

    # Iterate through processing each node.
    while len(openList) > 0:
        # Find the smallest element in the open list (using the estimatedTotalCost).
        currentRecord = min(openList, key=lambda r: r.estimatedTotalCost)

        # If it is the goal node, then terminate.
        if currentRecord.node == goal:
            break

        # Otherwise get its outgoing connections.
        connections = graph.getConnections(currentRecord.node)

        # Loop through each connection in turn.
        for connection in connections:
            # Get the cost estimate for the end node.
            endNode = graph.nodes[connection.toNode - 1]
            endNodeCost = currentRecord.costSoFar + connection.cost

            # If the node is closed we may have to skip, or remove it from the closed list.
            endNodeRecord = next((r for r in closedList if r.node == endNode), None)
            if endNodeRecord and endNodeRecord.costSoFar <= endNodeCost:
                continue

            # We can use the node’s old cost values to calculate its heuristic without calling the possibly expensive heuristic function.
            endNodeHeuristic = endNodeRecord.estimatedTotalCost - endNodeRecord.costSoFar if endNodeRecord else heuristic(
                start, endNode)

            # Skip if the node is open and we’ve not found a better route.
            endNodeRecord = next((r for r in openList if r.node.nodeNumber == endNode), None)
            if endNodeRecord and endNodeRecord.costSoFar <= endNodeCost:
                continue

            # Otherwise we know we’ve got an unvisited node, so make a record for it.
            if not endNodeRecord:
                endNodeRecord = NodeRecord(endNode, None, float('inf'), float('inf'))
                openList.append(endNodeRecord)

            # We’re here if we need to update the node. Update the cost, estimate and connection.
            endNodeRecord.costSoFar = endNodeCost
            endNodeRecord.connection = connection
            endNodeRecord.estimatedTotalCost = endNodeCost + endNodeHeuristic

        # We’ve finished looking at the connections for the current node, so add it to the closed list and remove it from the open list.
        openList.remove(currentRecord)
        closedList.append(currentRecord)

    # We’re here if we’ve either found the goal, or if we’ve no more nodes to search, find which.
    if currentRecord.node != goal:
        # We’ve run out of nodes without finding the goal, so there’s no solution.
        return list()

    else:
        # Compile the list of connections in the path.
        path = []
        while currentRecord.node != start:
            path.append(currentRecord.node.nodeNumber)
            currentRecord = next(r for r in closedList if r.node.nodeNumber == currentRecord.connection.fromNode)
        path.append(start.nodeNumber)
        # Reverse the path, and return it.
        path.reverse()
        return path


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
    start_node = graph.nodes[0]  # Replace 0 with the index-1 of the desired start node
    goal_node = graph.nodes[28]  # Replace 28 with the index-1 of the desired goal node
    path1 = pathfindAStar(graph, start_node, goal_node)
    path2 = pathfindAStar(graph, graph.nodes[0], graph.nodes[37])
    path3 = pathfindAStar(graph, graph.nodes[10], graph.nodes[0])
    path4 = pathfindAStar(graph, graph.nodes[32], graph.nodes[65])
    path5 = pathfindAStar(graph, graph.nodes[57], graph.nodes[42])

    with open('output.txt', 'w') as f:
        f.write('Nodes:\n')
        for node in graph.nodes:
            f.write(node.toString())
        f.write('Connections:\n')
        for connection in graph.connections:
            f.write(connection.toString())
        f.write('Path 1: ')
        f.write(str(path1))
        f.write('\nPath 2: ')
        f.write(str(path2))
        f.write('\nPath 3: ')
        f.write(str(path3))
        f.write('\nPath 4: ')
        f.write(str(path4))
        f.write('\nPath 5: ')
        f.write(str(path5))


if __name__ == '__main__':
    main()
