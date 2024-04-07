liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

import math


def contruct_graph():
    graph = {}

    for pair in liquidity:
        _from, to = pair[0], pair[1]
        if _from not in graph:
            graph[_from] = {}
        graph[_from][to] = -math.log(float(liquidity[pair][1]) / float(liquidity[pair][0]))
        if to not in graph:
            graph[to] = {}
        graph[to][_from] = -math.log(float(liquidity[pair][0]) / float(liquidity[pair][1]))
    return graph


# For each node prepare the destination and predecessor
def initialize(graph, source):
    dist = {}  # Stands for destination
    pred = {}  # Stands for predecessor
    for node in graph:
        dist[node] = float('Inf')  # We start admiting that the rest of nodes are very very far
        pred[node] = None
    dist[source] = 0  # For the source
    return dist, pred


def relax(u, v, graph, dist, pred):
    # If the distance between node u and node v is lower than the one I have now
    if dist[u] + graph[u][v] < dist[v]:
        # Record this lower distance
        dist[v] = dist[u] + graph[u][v]
        pred[v] = u


def backtrace_negative_loop(pred, source):
    arbitrageLoop = [source]
    next_node = source
    while True:
        next_node = pred[next_node]
        if next_node not in arbitrageLoop:
            arbitrageLoop.append(next_node)
        else:
            # A loop is found
            arbitrageLoop.append(next_node)
            arbitrageLoop = arbitrageLoop[arbitrageLoop.index(next_node):]
            arbitrageLoop.reverse()
            return arbitrageLoop

def bellman_ford(graph, source):
    dist, pred = initialize(graph, source)
    for i in range(len(graph) - 1):  # Relax each edge |V| - 1 times
        for u in graph:
            for v in graph[u]:  # For each neighbour of u
                relax(u, v, graph, dist, pred)  # relax

    # Check for negative-weight cycles
    for u in graph:
        for v in graph[u]:
            if dist[v] < dist[u] + graph[u][v]:
                return backtrace_negative_loop(pred, source)
    # Return the negative-weight cycle if found, else return None
    return None


if __name__ == '__main__':
    startToken = 'tokenB'
    graph = contruct_graph()
    paths = {}
    for src in graph:
        path = bellman_ford(graph, src)
        if path is None:
            break
        if path[0] != src:
            path.insert(0, src)
        if path[-1] != src:
            path.append(src)
        paths[src] = path


    if startToken in paths:
        path = paths[startToken]
        balance = 5
        #print(f"Starting with {balance} in {path[0]} ")
        for i, value in enumerate(path):
            if i + 1 < len(path):
                _from = path[i]
                to = path[i + 1]
                rate = math.exp(-graph[_from][to])
                balance *= rate
                #print(f"{_from} to {to} at {rate} = {balance}")
        
        # Print the result
        str = f'path: {path[0]}'
        for i in range(1, len(path)):
            str += f'-> {path[i]}'
        str += f", {startToken} balance={balance}"
        print(str)
    else:
        print("No opportunity here :(")
        