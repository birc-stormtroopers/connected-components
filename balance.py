"""
Building connected components using a tree representation.

This time we balance the trees, in an attempt to make the paths
shorter. You can do this either by rank (length from root to leaves)
or size (number of nodes in a tree) and either will balance the trees
to O(log k) for trees of size/rank k. (This isn't a general case for
trees of size k, but it is when we build them by making the smaller tree
a subtree of the larger).
"""

from __future__ import annotations
from typing import NewType, Union, TypeGuard, cast

# The following is just for annotating the code to keep track of the
# kind of objects we are working with. It does not affect the function
# of any of the functions.

# Nodes are represented as integers.
Node = NewType('Node', int)
# Edges are pairs of nodes.
Edge = NewType('Edge', tuple[Node, Node])
# A tree size is also just an integer
Size = NewType('Size', int)
# Components are represented by a forest of trees. Roots do not
# store a parent node but rather a Size, and we use negative
# numbers to recognise those.
Forest = NewType('Forest', list[Union[Node, Size]])


def is_size(v: Node | Size) -> TypeGuard[Size]:
    """Check if v is size."""
    return v < 0


def is_node(v: Node | Size) -> TypeGuard[Node]:
    """Check if v is a node."""
    return v >= 0


def size(v: Node | Size) -> int:
    """Cast sizes to integers."""
    assert is_size(v)
    return -int(v)


def to_size(v: int) -> Size:
    """Cast integers to sizes."""
    return Size(-v)


def root(f: Forest, v: Node) -> Node:
    """Locate the root of v's forest."""
    parent = f[v]
    while is_node(parent):
        v, parent = parent, f[parent]
    return v


def union(f: Forest, v: Node, w: Node) -> None:
    """Merge v's and w's components and update comp accordingly."""
    # Get the components of the two nodes.
    root_v, root_w = root(f, v), root(f, w)
    if root_v == root_w:
        return  # They are already in the same component

    # Make one's root point to the other. Make the one with
    # the largest size the parent.
    size_w, size_v = size(f[root_w]), size(f[root_v])
    new_size = to_size(size_w + size_v)

    # make the larger tree the root
    if size_w < size_v:
        root_v, root_w = root_w, root_v
    f[root_v] = root_w
    f[root_w] = new_size


def components(n: int, edges: list[Edge]) -> Forest:
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
    # Initially, each node has its own component of size 1
    components = Forest([to_size(1) for i in range(n)])
    for v, w in edges:
        assert 0 <= v < n and 0 <= w < n
        union(components, v, w)

    return components
