import heapq

def makeGraph(fileName):
    graph = {}
    heuristic = {}
    file = open(fileName, 'r')
    for i in file:
        line = i.strip().split(' ')
        graph[line[0]] = []
        heuristic[line[0]] = int(line[1])
        for j in range(2, len(line), 2):
            graph[line[0]].append((line[j], int(line[j+1])))
    return graph, heuristic

def A_star_search(graph, heuristic, start, destination):
    fringe = [(heuristic[start], start)]
    path_cost = {start : 0}
    popped = []
    popped_names = []
    parent = {(heuristic[start], start) : None}
    heapq.heapify(fringe)
    node = (0, '')
    while node[1] != destination:
        try:
            node = heapq.heappop(fringe)
        except:
            return "NO PATH FOUND"
        popped.append(node)
        popped_names.append(node[1])
        for i in (graph[node[1]]):
            if i[0] not in popped_names:
                cost = path_cost[node[1]] + i[1]
                path_cost[i[0]] = cost
                total_cost = heuristic[i[0]] + cost
                heapq.heappush(fringe, (total_cost, i[0]))
                parent[(total_cost, i[0])] = node
    

    path = [destination]
    current = popped[len(popped)-1]
    while current != (heuristic[start], start):
        current = parent[current]
        if current in popped:
            path.append(current[1])        
    path.reverse()
    str1 = 'Path: '
    for i in range (len(path)):
        if i != len(path) - 1:
            str1+= f"{path[i]} -> "
        else:
            str1 += path[i] + '\n'
    str1+=f"Total distance: {popped[len(popped)-1][0]} km"
    print(popped)
    print(parent)
    return str1






g, h = makeGraph('Input file.txt')
s = input('Start node: ')
d = input('Destination: ')
A_S  = A_star_search(g, h, s, d)
print(A_S)
