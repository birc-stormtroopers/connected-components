"""
Explore all cities we can reach from A.
"""


def build_neighbours(
    n: int,
    edges: list[tuple[int, int]]
) -> list[set[int]]:
    """Collect sets of neighbours for each node."""
    neighbours: list[set[int]] = [set() for _ in range(n)]
    for v, w in edges:
        neighbours[v].add(w)
        neighbours[w].add(v)
    return neighbours


def reachable(a: int, neighbors: list[set[int]]) -> set[int]:
    """Collect all cities reachable from `a`."""
    seen, unprocessed = {a}, {a}
    while unprocessed:
        v = unprocessed.pop()  # process the next city
        for w in neighbors[v]:
            if w not in seen:
                seen.add(w)
                unprocessed.add(w)
    return seen


neighbours = build_neighbours(5, [(0, 1), (2, 1), (3, 4)])
print(reachable(1, neighbours))
print(reachable(3, neighbours))
