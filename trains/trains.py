import tkinter
from math import pi , acos , sin , cos
import sys
from collections import deque
from heapq import heappush, heappop, heapify
from time import perf_counter
import random

cont = True

def calcd(node1, node2):
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees
    y1, x1 = node1
    y2, x2 = node2

    R   = 3958.76 # miles = 6371 km
    y1 *= pi/180.0
    x1 *= pi/180.0
    y2 *= pi/180.0
    x2 *= pi/180.0

    # approximate great circle distance with law of cosines
    return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

def dijkstra(start,end):
    closed = set()
    start_node = (0, start, [start])
    fringe = []
    num = 0
    heappush(fringe, start_node)
    while fringe:
        v = heappop(fringe)
        depth, state, path = v
        if state == end:
            root.update()
            return (depth, path)
        if state not in closed:
            closed.add(state)
            for c in graph[state]:
                child, distance = c
                if child not in closed:
                    canvas.itemconfig(lines[(state, child)], fill="red") 
                    num+=1 
                    changed_lines.append(lines[(state, child)])
                    if num % 1000 == 0:
                        root.update()
                    temp = (depth + distance, child, path+[child])
                    heappush(fringe, temp)
    return None

def a_star(start,end):
    closed = set()
    start_node = (calcd(nodes[start], nodes[end]), 0, start, [start])
    fringe = []
    num = 0
    heappush(fringe, start_node)
    while fringe:
        v = heappop(fringe)
        estimite, depth, state, path = v
        if state == end:
            root.update()
            return depth, path
        if state not in closed:
            closed.add(state)
            for c in graph[state]:
                child, distance = c
                if child not in closed:
                    num +=1
                    canvas.itemconfig(lines[(state, child)], fill="orange") 
                    changed_lines.append(lines[(state, child)])
                    if num % 300 == 0:
                        root.update()
                    temp = (depth + calcd(nodes[child], nodes[end])+distance, depth + distance, child, path+[child])
                    heappush(fringe, temp)
    return None

def DFS(start, end):
    fringe = deque()
    visited = set()
    fringe.append((start,[], 0))
    visited.add(start)
    num = 0
    while fringe:
        v, prev, depth = fringe.pop()
        if v == end: #it might be 32 instead of 31
            #root.update()
            return depth, prev
        for child in graph[v]:
            c, dis = child
            if c not in visited:
                canvas.itemconfig(lines[(v, c)], fill="yellow") 
                num+=1 
                changed_lines.append(lines[(v, c)])
                if num % 100 == 0:
                    root.update()
                fringe.append((c, prev + [c], depth+dis))
                visited.add(c)

def kDFS(start, end, k):
    num = 0
    fringe = [(start,0,set(), 0)]
    while fringe:
        v, depth, ancestor, distance = fringe.pop()
        if v == end:
            root.update()
            return distance, ancestor
        if depth < k:
            for child in graph[v]:
                c, dis = child
                if c not in ancestor :
                    num +=1
                    canvas.itemconfig(lines[(v, c)], fill="red") 
                    changed_lines.append(lines[(v, c)])
                    if num % 750 == 0:
                        root.update()
                    ances = ancestor.copy()
                    ances.add(c)
                    fringe.append((c, depth+1, ances, distance+dis))
    root.update()
    return None

def ID_DFS(start, end):
    max_depth = 0
    result = None
    while result is None:
        changed_lines = []
        result = kDFS(start, end, max_depth)
        max_depth = max_depth + 50
        for l in changed_lines:
            canvas.itemconfig(l, fill="black") 
        #turn all lines black
    return result


def Bidirectional_Dijkstra(start, end):
    if start == end:
        return (0, [start, end])
    start_fringe = []
    start_visited = set()
    start_node = (0, start, [start])
    heappush(start_fringe, start_node)
    start_num = 0
    #start_visited.add(start)
    end_fringe = []
    end_visited = set()
    end_node = (0,end, [end])
    end_num = 0
    smallest_start = sys.maxsize
    smallest_end = sys.maxsize
    smallest_start_fringe = []
    smallest_end_fringe = []
    heappush(end_fringe, end_node)
    #end_visited.add(end)
    while start_fringe or end_fringe:
        #start_depth, start_v, start_list = heappop(start_fringe)
        #end_depth, end_v, end_list = heappop(end_fringe)
        if start_fringe:
            start_depth, start_v, start_list = heappop(start_fringe)
            if start_v not in start_visited and start_depth <= smallest_start:
                start_visited.add(start_v)
                for c in graph[start_v]:
                    child, distance = c
                    #if child not in start_visited:
                    if child in end_visited:
                        root.update()
                        if (depth:= start_depth+distance) < smallest_start:
                            smallest_start = start_depth
                            smallest_start_fringe = start_list + [child]
                            #return start_depth+ end_depth + distance, start_list + end_list
                    canvas.itemconfig(lines[(start_v, child)], fill="blue") 
                    start_num+=1 
                    changed_lines.append(lines[(start_v, child)])
                    if start_num % 1000 == 0:
                        root.update()
                    heappush(start_fringe,((start_depth + distance, child, start_list + [child])))
                        #start_visited.add(child)
        if end_fringe:
            end_depth, end_v, end_list = heappop(end_fringe)
            if end_v not in end_visited and end_depth <= smallest_end:
                end_visited.add(end_v)
                for c in graph[end_v]:
                    child, distance = c
                    #if child not in end_visited:
                    if child in start_visited:
                        root.update()
                        if (depth:= end_depth+distance) < smallest_end:
                            smallest_end = end_depth
                            smallest_end_fringe = end_list
                            #return start_depth + end_depth+distance, start_list + end_list
                    canvas.itemconfig(lines[(end_v, child)], fill="blue") 
                    end_num+=1 
                    changed_lines.append(lines[(end_v, child)])
                    if end_num % 1000 == 0:
                        root.update()
                    heappush(end_fringe,((end_depth + distance, child, [child] + end_list)))
                        #end_visited.add(child)
    return smallest_start +smallest_end, smallest_start_fringe + smallest_end_fringe

def Reverse_Astar(start, end):
    closed = set()
    start_node = (-1*calcd(nodes[start], nodes[end]), 0, start, [start])
    fringe = []
    heappush(fringe, start_node)
    num = 0
    while fringe:
        v = heappop(fringe)
        estimite, depth, state, path = v
        if state == end:
            root.update()
            return depth, path
        if state not in closed:
            closed.add(state)
            for c in graph[state]:
                child, distance = c
                if child not in closed:
                    canvas.itemconfig(lines[(state, child)], fill="cyan") 
                    num+=1 
                    changed_lines.append([(state, child)])
                    if num % 100 == 0:
                        root.update()
                    temp = (-1*depth - calcd(nodes[child], nodes[end])-distance, depth + distance, child, path+[child])
                    heappush(fringe, temp)
    return None

def random_search(start, end):
    fringe = []
    visited = set()
    fringe.append((start,[], 0))
    visited.add(start)
    num = 0
    while fringe:
        v, prev, depth = fringe.pop(random.randrange(len(fringe))) 
        if v == end: 
            root.update()
            return depth, prev
        for child in graph[v]:
            c, dis = child
            if c not in visited:
                canvas.itemconfig(lines[(v, c)], fill="magenta") 
                num+=1 
                changed_lines.append(lines[(v, c)])
                if num % 1500 == 0:
                    root.update()
                fringe.append((c, prev + [c], depth+dis))
                visited.add(c)
    
changed_lines = []
with open("trains/rrNodes.txt") as f:
    node_list = [l.strip() for l in f]
    nodes = dict()
    for line in node_list:
        split = line.split()
        nodes[split[0]] = (float(split[1]), float(split[2]))
    #nodes = {split:=line.split()[0]: split[1:] for line in node_list}
        
with open("trains/rrNodeCity.txt") as f:
        nodecity_list = [l.strip() for l in f]
        node_city = dict()
        for line in nodecity_list:
            n = line.split()
            if len(n) > 2:
                node_city[n[1] + " " + n[2]] = n[0]
            else: 
                node_city[n[1]] = n[0]

print("Enter departing city: ", end="")
city1 = input()
print("Enter destination: ", end="")
city2= input()
while cont:
    print("1. Dijkstra\n2. A*\n3. DFS\n4. Bidirectional Dijsktra\n5.ID-DFS(takes too long)\n6. Reverse A*\n7. Random\nPick which algorithm to use (#) or -1 to exit: ", end="")

    algo = input()

    if algo == "-1":
        cont = False
        break

    root = tkinter.Tk()
    canvas = tkinter.Canvas(root, height=1000, width=1000, bg='white') 
    lines = dict()

    with open("trains/rrEdges.txt") as f:
        edge_list = [l.strip() for l in f]
        graph = dict()
        vis_graph = set()
        for line in edge_list:
            e = line.split()
            dis = calcd(nodes[e[0]], nodes[e[1]])
            ey, ex = nodes[e[0]]
            eey, eex = nodes[e[1]]
            if e[0] in vis_graph:
                graph[e[0]] += [(e[1], dis)]
            else:
                graph[e[0]] = [(e[1], dis)]
                vis_graph.add(e[0])
            if e[1] in vis_graph:
                graph[e[1]] += [(e[0], dis)]
            else:
                graph[e[1]] = [(e[0], dis)]
                vis_graph.add(e[1])
            cc = [(1000-(abs(ex+55)*11), 525-((ey-25)*15)), (1000-(abs(eex+55)*11), 525-((eey-25)*15))]
            l = canvas.create_line(cc, tag='grid_line')
            lines[(e[0], e[1])] = l
            lines[(e[1], e[0])] = l
    canvas.pack(expand=True)
    root.update()
    #city1 = sys.argv[1]
    #city2 = sys.argv[2]

    if algo == "1":
        d, p = dijkstra(node_city[city1],node_city[city2])

    elif algo == "2":
        d, p = a_star(node_city[city1],node_city[city2])

    elif algo == "3":
        d, p = DFS(node_city[city1],node_city[city2])

    elif algo == "4":
        d, p = Bidirectional_Dijkstra(node_city[city1],node_city[city2])

    elif algo == "5":
        d, p = ID_DFS(node_city[city1],node_city[city2])

    elif algo == "6":
        d, p = Reverse_Astar(node_city[city1],node_city[city2])
    elif algo == "7":
        d, p = random_search(node_city[city1],node_city[city2])

    for i in range(0,len(p)-1):
        if p[i] != p[i+1]:
            canvas.itemconfig(lines[(p[i], p[i+1])], fill="green", width="5")
    root.update()
    root.mainloop()

    print("Try another algorithm")

