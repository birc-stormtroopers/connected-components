"""
Building connected components using simple union-find operations.

Each update runs in O(n) so with O(m) edges the total running time is O(nm).
"""


def union(comp: list[int], v: int, w: int) -> None:
    """Merge v's and w's components and update comp accordingly."""
    cv, cw = comp[v], comp[w]
    for u, cu in enumerate(comp):
        if cu == cw:
            comp[u] = cv


def components(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """
    Compute connected components.

    Compute the connected components for n nodes based on the
    edges. All the nodes listed in the edges must be values in
    the range 0 <= ... < n.

    >>> comp = components(5, [(2, 1), (0, 1), (3, 4)])
    >>> assert comp[0] == comp[1] and comp[1] == comp[2]
    >>> assert comp[3] == comp[4]
    >>> assert comp[0] != comp[3]
    """
    # Initially, each node has its own component
    components = list(range(n))
    for v, w in edges:
        assert 0 <= v < n and 0 <= w < n
        union(components, v, w)

    return components
