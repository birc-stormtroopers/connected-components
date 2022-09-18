"""
Building connected components using a tree representation.

This time we balance the trees, in an attempt to make the paths
shorter. You can do this either by rank (length from root to leaves)
or size (number of nodes in a tree) and either will balance the trees
to O(log k) for trees of size/rank k. (This isn't a general case for
trees of size k, but it is when we build them by making the smaller tree
a subtree of the larger).
"""


def is_size(v: int) -> bool:
    """Check if v is size."""
    return v < 0


def is_node(v: int) -> bool:
    """Check if v is a node."""
    return v >= 0


def size(v: int) -> int:
    """Cast sizes to integers."""
    assert is_size(v)
    return -v


def to_size(v: int) -> int:
    """Cast integers to sizes."""
    return -v


def root(f: list[int], v: int) -> int:
    """Locate the root of v's forest."""
    parent = f[v]
    while is_node(parent):
        v, parent = parent, f[parent]
    return v


def union(f: list[int], v: int, w: int) -> None:
    """Merge v's and w's components and update comp accordingly."""
    root_v, root_w = root(f, v), root(f, w)
    size_w, size_v = size(f[root_w]), size(f[root_v])
    new_size = to_size(size_w + size_v)

    # make the larger tree the root
    if size_w < size_v:
        root_v, root_w = root_w, root_v
    f[root_v] = root_w
    f[root_w] = new_size


def components(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """
    Compute connected components.

    Compute the connected components for n nodes based on the
    edges. All the nodes listed in the edges must be values in
    the range 0 <= ... < n.

    >>> comp = components(5, [(0, 1), (2, 1), (3, 4)])
    >>> assert root(comp, 0) == root(comp, 1)
    >>> assert root(comp, 1) == root(comp, 2)
    >>> assert root(comp, 3) == root(comp, 4)
    >>> assert root(comp, 0) != root(comp, 3)
    """
    components = [to_size(1) for i in range(n)]
    for v, w in edges:
        assert 0 <= v < n and 0 <= w < n
        union(components, v, w)
    return components
