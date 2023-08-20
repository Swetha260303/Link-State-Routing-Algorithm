import os
from collections import deque, namedtuple
from random import seed
from random import random
seed(1)

# we'll use infinity as a default distance to nodes. inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')
pathlist=[]
router_matrix = []
matrix_set = 0
nodes = []
distances = {}
unvisited = {}
previous = {}
visited = {}
interface = {}
path = []
start = 0
end = 0
def make_edge(start, end, cost=1): 
    return Edge(start, end, cost)
def print_choices():
    os.system("figlet Link State Routing Simulator")
    print("\n######################################################\n")
    print("(1) Input Network Topology File")
    print("(2) Build a Connection Table")
    print("(3) Shortest Path to Destination Router")
    print("(4) Exit")
    print("\n######################################################\n") 
    pass
# Function to check if entered command is valid or not - i.e. : # 1: Should be a digit.
# 2: Should be from the range of given choices.
def check_choices(command): 
    if not command.isdigit():
        print("Please enter a number as command from given choices..")
        return -1 
    else:
        command = int(command)
        if command > 4 or command < 1 :
            print("Please enter a valid command from given choices..") 

            return -1 
        else:
            return command
# Function to process the given input file. 
def process_file(fname):
    print("process_file")
    global matrix_set 
    global router_matrix 
    matrix_set = 0 
    router_matrix = []
    with open(fname) as f:
        print("All good here ")
        path=router_matrix=[list(map(str,x.split()))for x in f]
        print("list :",router_matrix)
    for k in path:
        (s,d,w)=k
        pathlist.append((s,d,int(w))) 
    print("\nReview original topology matrix:\n") 
    print(pathlist)
# Function to store the distances in dictionary format.
class Graph:
    def __init__(self,pathlist):
# let's check that the data is right
        wrong_edges = [i for i in pathlist if len(i) not in [2, 3]] 
        if wrong_edges:
# Data from input file is stored in a two
            raise ValueError('Wrong edges data: {}'.format(wrong_edges)) 
        self.pathlist = [make_edge(*path) for path in pathlist]
    @property
    def vertices(self):
        return set( sum(([edge.start, edge.end] for edge in self.pathlist), [] ))
    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs
    def remove_edge(self, n1, n2, both_ends=True): 
        node_pairs = self.get_node_pairs(n1, n2, both_ends) 
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs: 
                self.edges.remove(edge)
    def add_edge(self, n1, n2, cost=1, both_ends=True):     

        node_pairs = self.get_node_pairs(n1, n2, both_ends) 
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))
        self.edges.append(Edge(start=n1, end=n2, cost=cost)) 
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))
    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices} 
        for path in self.pathlist:
            neighbours[path.start].add((path.end, path.cost))
        return neighbours
    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist' 
        distances = {vertex: int for vertex in self.vertices} 
        previous_vertices = {
            vertex: None for vertex in self.vertices }
        distances[source] = 0
        vertices = self.vertices.copy()
        total=0
        while vertices:
            current_vertex = min(vertices,key=lambda vertex:distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == int:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost + random() # random for queue time
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex
                    total+=alternative_route
            print("Total End-End Time = ",total,"ms")
        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path
if __name__ == "__main__":
    print_choices()
    command = 0
# Run till user wants to exit.
    while command !=4 :
        command = check_choices(input("Choice: ")) # Accept the topology file.
        if command == 1:
            if matrix_set == 1:
                answer = input("\nThe network topology is already uploaded. Do you want to overwrite?(Y/N) :")
            if matrix_set == 0 or answer == 'Y' or answer == 'y':
                filename = input("\nInput original network topology matrix data file[ NxN distance matrix. (value : -1 for no link, 0 for self loop) : ")
                if os.path.isfile(filename):
                    process_file(filename)
                    start = 0
                    end = 0
                    graph = Graph(pathlist)
                    matrix_set=1
                else:
                    print("\nThe file does not exist. Please try again..")
        # Accept the source router and display the connection table.
        elif command == 2:
            if matrix_set == 1 :
                start = input("\nSelect the current hop : ")
                print("\nNext-Hop Weight")
                for key in pathlist:
                    # print(key,"\t\t", interface[key])
                    if(key[0]==start):
                        print(key[1],key[2])
                else:
                    start = 0
                    print("\nPlease enter a valid source router.")
            else:
                print("\nNo network topology matrix exist. Please upload the data file first.. ") # Accept the destination router and display the shortest path and cost.
        elif command == 3:
            if matrix_set == 1 :
                start = input("\nSelect a source router : ")
                end = input("\nSelect a destination router : ")
                print("start:- ",start)
                print("end:- ",end)
                path=graph.dijkstra(start,end)  
                route=""
                c=0
                print(len(path))
                for hop in path:
                    c+=1
                    if(c<len(path)):
                        route+=hop+"->"
                    else:

                        route+=hop
                    print(route)
    # print(graph.dijkstra("a", "e"))
