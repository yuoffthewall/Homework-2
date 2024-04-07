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

def perm(start, path, paths):
    if start == len(path):
        paths.append(path.copy())
        return
    for i in range(start, len(path)):
        path[start], path[i] = path[i], path[start]
        perm(start + 1, path, paths)
        path[start], path[i] = path[i], path[start]


def comb(n, k, start, path, paths):
    for i in range(start, n - k + 1):
        path.append(i)
        if k == 1:
            perm(0, path, paths)
        else:
            comb(n, k - 1, i + 1, path, paths)
        path.pop()
            

# All possible paths in [0, n]
def generate_paths(n):
    path, paths = [], []
    for k in range(1, n + 1):
        comb(n, k, 0, path, paths)
    return paths


# Deposit y get x
def swap(tin, tout, amount_in):
    x, y = 0, 0
    if (tin, tout) in liquidity:
        pair = (tin, tout)
        x, y = liquidity[pair][1], liquidity[pair][0]
    else:
        pair = (tout, tin)
        x, y = liquidity[pair][0], liquidity[pair][1]
    
    amount_out = (0.997 * x * amount_in) / (y + 0.997 * amount_in)
    return amount_out


def arbitrage(startToken, balance, path):
    for i in range(len(path) - 1):
        tin, tout = path[i], path[i + 1]
        balance = swap(tin, tout, balance)
    return balance


if __name__ == '__main__':
    startToken = 'tokenB'    
    tokens = ['tokenA', 'tokenB', 'tokenC', 'tokenD', 'tokenE']
    tokens.remove(startToken)
    paths = generate_paths(len(tokens))
    balance = 5
    for p in paths:
        path = [tokens[p[i]] for i in range(len(p))]
        path.insert(0, startToken)
        path.append(startToken)
        new_balance = arbitrage(startToken, balance, path)
        
        if new_balance < 20:
            continue
        
        # Print the result
        str = f'path: {path[0]}'
        for i in range(1, len(path)):
            str += f'-> {path[i]}'
        str += f", {startToken} balance={new_balance}"
        print(str)