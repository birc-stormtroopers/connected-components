"""
Building connected components using a tree representation.

The speed of the operations depends on the depth of the trees
and we do not balancing in this version, so we can still
potentially run in O(nm).
"""


def is_root(f: list[int], v: int) -> bool:
    """Return True if v is a root."""
    return f[v] == -1


def root(f: list[int], v: int) -> int:
    """Locate the root of v's forest."""
    while not is_root(f, v):
        v = f[v]
    return v


def union(f: list[int], v: int, w: int) -> None:
    """Merge v's and w's components and update comp accordingly."""
    f[root(f, v)] = root(f, w)


def components(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """
    Compute connected components.

    Computes the connected components for n nodes based on the
    edges. All the nodes listed in the edges must be values in
    the range 0 <= ... < n.

    >>> comp = components(5, [(0, 1), (2, 1), (3, 4)])
    >>> assert root(comp, 0) == root(comp, 1)
    >>> assert root(comp, 1) == root(comp, 2)
    >>> assert root(comp, 3) == root(comp, 4)
    >>> assert root(comp, 0) != root(comp, 3)
    """
    components = [-1] * n
    for v, w in edges:
        assert 0 <= v < n and 0 <= w < n
        union(components, v, w)
    return components
