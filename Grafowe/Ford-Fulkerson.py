from collections import deque

G = [
    [[1, 16], [2, 13]],
    [[2, 10], [3, 12]],
    [[1, 4], [4, 14]],
    [[2, 9], [5, 20]],
    [[3, 4], [5, 7]],
    [],
]


def tworzenie_macierzy(G: list[list[list[int]]]) -> list[list[int]]:
    n = len(G)
    macierz = [[0 for _ in range(n)] for _ in range(n)]

    for wierzcholek, lista in enumerate(G):
        for child, weight in lista:
            macierz[wierzcholek][child] = weight

    return macierz


def ford_fulkerson(G: list[list[list[int]]], s: int, t: int):
    result = 0
    n = len(G)
    MS = tworzenie_macierzy(G)

    def bfs():
        parent = [-1 for _ in range(n)]
        visited = [False for _ in range(n)]
        visited[s] = True

        Q = deque()
        Q.append(s)

        while Q:
            vert = Q.popleft()

            if vert == t:
                return parent

            for child in range(n):
                if not visited[child] and MS[vert][child] > 0:
                    visited[child] = True
                    parent[child] = vert
                    Q.append(child)

        return None

    while True:
        parent = bfs()

        if parent is None:
            break

        vert = t
        min_capacity = float("inf")

        while vert != s:
            rodzic = parent[vert]
            min_capacity = min(min_capacity, MS[rodzic][vert])
            vert = rodzic

        vert = t
        while vert != s:
            rodzic = parent[vert]
            MS[rodzic][vert] -= min_capacity
            MS[vert][rodzic] += min_capacity
            vert = rodzic

        result += min_capacity

    return result


if __name__ == "__main__":
    print(ford_fulkerson(G, 0, 5))
