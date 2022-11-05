from cProfile import label
import queue
from turtle import color, distance
import matplotlib.pyplot as plt

def getHeuristics():
    heuristics = {}
    f = open("heuristics.txt")
    for i in f.readlines():
        node_hetristics_val = i.split()
        heuristics[node_hetristics_val[0]] = int(node_hetristics_val[1])

    return heuristics

def getCity():
    city = {}
    citiesCode = {}
    f = open("cities.txt")
    j = 1
    for i in f.readlines():
        node_city_val = i.split()
        city[node_city_val[0]] = [int(node_city_val[1]), int(node_city_val[2])]

        citiesCode[j] = node_city_val[0]
        j += 1
    return city, citiesCode


def createGraph():
    graph = {}
    file = open("citiesGraph.txt")
    for i in file.readlines():
        node_val = i.split()

        if node_val[0] in graph and node_val[1] in graph:
            c = graph.get(node_val[0])
            c.append([node_val[1], node_val[2]])
            graph.update({node_val[0]: c})

            c = graph.get(node_val[1])
            c.append([node_val[0], node_val[2]])
            graph.update({node_val[1]: c})

        elif node_val[0] in graph:
            c = graph.get(node_val[0])
            c.append([node_val[1], node_val[2]])
            graph.update({node_val[0]: c})

            graph[node_val[1]] = [[node_val[0], node_val[2]]]

        elif node_val[1] in graph:
            c = graph.get(node_val[1])
            c.append([node_val[0], node_val[2]])
            graph.update({node_val[1]: c})

            graph[node_val[0]] = [[node_val[1], node_val[2]]]
        
        else:
            graph[node_val[0]] = [[node_val[1], node_val[2]]]
            graph[node_val[1]] = [[node_val[0], node_val[2]]]
    return graph


def GBFS(startnode, heuristics, graph, goalNode):
    priorityQueue = queue.PriorityQueue()
    priorityQueue.put((heuristics[startnode], startnode))

    path = []

    while priorityQueue.empty() == False:
        current = priorityQueue.get()[1]
        path.append(current)

        if current == goalNode:
            break

        priorityQueue = queue.PriorityQueue()

        for i in graph[current]:
            if i[0] not in path:
                priorityQueue.put((heuristics[i[0]], i[0]))

    return path

def browser(startNode, graph):
    visited = {}
    frontier = queue.Queue()

    visited[startNode] = 0
    frontier.put(startNode)
    
    while frontier.empty() == False:
        current_node = frontier.get()

        for node in graph[current_node]:
            if node[0] not in visited:
                frontier.put(node[0])
                visited[node[0]] = 0
            
    return visited


def Astar(startNode, heuristics, graph, goalNode):
    priorityQueue = queue.PriorityQueue()
    listNode = browser(startNode, graph)
    distance = 0 
    path = []

    priorityQueue.put((int(heuristics[startNode]) + distance, [startNode, 0]))

    while priorityQueue.empty() == False:
        current = priorityQueue.get()
        listNode[current[1][0]] = current[0]
        path.append(current[1][0])
        distance += int(current[1][1])

        if current[1][0] == goalNode:
            break

        priorityQueue = queue.PriorityQueue()

        for i in graph[current[1][0]]:
            if i[0] not in path:
                priorityQueue.put((int(heuristics[i[0]]) + int(i[1]) + distance, i))
            elif listNode[i[0]] > int(heuristics[i[0]]) + int(i[1]) + distance:
                listNode[i[0]] = int(heuristics[i[0]]) + int(i[1]) + distance
                priorityQueue.put((int(heuristics[i[0]]) + int(i[1]) + distance, i))
        print(priorityQueue)

    return path

def drawMap(city, gbfs, astar, graph):
    for i, j in city.items():
        plt.plot(j[0], j[1], "ro")
        plt.annotate(i, (j[0] + 5, j[1]))

        for k in graph[i]:
            n = city[k[0]]
            plt.plot([j[0], n[0]], [j[1], n[1]], "gray")

    for i in range(len(gbfs)):
        try:
            first = city[gbfs[i]]
            secend = city[gbfs[i + 1]]

            plt.plot([first[0], secend[0]], [first[1], secend[1]], "green")
        except:
            continue

    for i in range(len(astar)):
        try:
            first = city[astar[i]]
            secend = city[astar[i + 1]]

            plt.plot([first[0], secend[0]], [first[1], secend[1]], "blue")
        except:
            continue

    plt.errorbar(1, 1, label="GBFS", color="green")
    plt.errorbar(1, 1, label="ASTAR", color="blue")
    plt.legend(loc="lower left")

    plt.show()


if __name__ == "__main__":
    heuristics = getHeuristics()
    graph = createGraph()
    city, citiesCode = getCity()

    for i, j in citiesCode.items():
        print(i, j)

    while True:
        inputCode1 = int(input("Nhập đỉnh bắt đầu: "))
        inputCode2 = int(input("Nhập đỉnh kết thúc: "))

        if inputCode1 == 0 or inputCode2 == 0:
            break

        startCity = citiesCode[inputCode1]
        endCity = citiesCode[inputCode2]

        gbfs = GBFS(startCity, heuristics, graph, endCity)
        astar = Astar(startCity, heuristics, graph, endCity)
        print("GBFS => ", gbfs)
        print("ASTAR => ", astar)

        drawMap(city, gbfs, astar, graph)
