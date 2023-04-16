"""
Class: CS 330
Authors: Adam Johnson & Erik Overberg
Program: Assignment 3
"""

from typing import List
from heapq import heappush, heappop
from math import inf

class Graph:
    def __init__(self, connections):
        self.connections = connections
    
    def getConnections(self, node):
        return [c for c in self.connections if c.fromNode == node]

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

"""Defining function for A* Algorithm"""
def pathfind_AStar(graph, start, goal, heuristic):
    
    class NodeRecord:
        def __init__(self, node, connection: str = None, cost_so_far=inf, estimated_total_cost=inf):
            self.node = node
            self.connection = connection
            self.cost_so_far = cost_so_far
            self.estimated_total_cost = estimated_total_cost
            
        def __lt__(self, other):
            return self.estimated_total_cost < other.estimated_total_cost
    
    
    """initialize the record for start node"""
    start_record = NodeRecord(start, cost_so_far=0, estimated_total_cost=heuristic.estimate(start))
    """Initialize the open and closed lists"""
    open_list = [start_record]
    closed_list = []
    
    """Itirate through processing each node"""
    while open_list:
        """Find the smallest eleement in the open list using estimated_total_cost"""
        current = heappop(open_list)
        
        """If it is the goal node, then terminate"""
        if current.node == goal:
            """exit loop when goal node is smallest"""
            break
        closed_list.append(current)
        
        """otherwise get its outgoing connections"""
        connections = graph.get_connections(current.node)
        
        """Loop through each connection"""
        for connection in connections:
            """Get the cost estimate for the end node"""
            to_node = connection.to_node
            """TO node estimated cost"""
            to_node_cost = current.cost_so_far + connection.cost
            
            """if the node is closed we may have to skip, or remove it from the closed list"""
            to_node_record = next((nr for nr in closed_list if nr.node == to_node), None)
            if to_node_record and to_node_record.cost_so_far <= to_node_cost:
                continue
            
            to_node_record = next((nr for nr in open_list if nr.node == to_node), None)
            if to_node_record and to_node_record.cost_so_far <= to_node_cost:
                continue
            
            if to_node_record:
                closed_list.remove(end_node_record)
            
            """We can use the node's old cost values to calculate its heuristic without 
            calling the possibly expensive heuristic function"""
            to_node_heuristic = heuristic.estimate(to_node)
            if not to_node_record:
                to_node_record = NodeRecord(to_node)
                open_list.append(to_node_record)
            
            
            to_node_record.cost_so_far = to_node_cost
            to_node_record.connection = connection
            to_node_record.estimated_total_cost = to_node_cost + to_node_heuristic
        
        open_list.sort()
            
    else:
        """Goal cant be reached from the start """
        return None 
            
    
    """work back along the path, accumulating connections"""
    path: List[Connection] = []
    while current.node != start:
        path.append(current.connection)
        current = current.connection.from_node
    return list(reversed(path))
    
    