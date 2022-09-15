"""
Building connected components using a tree representation.

The speed of the operations depends on the depth of the trees
and we do not balancing in this version, so we can still
potentially run in O(nm).
"""

from typing import NewType

# The following is just for annotating the code to keep track of the
# kind of objects we are working with. It does not affect the function
# of any of the functions.

# Nodes are represented as integers.
Node = NewType('Node', int)
# Edges are pairs of nodes.
Edge = NewType('Edge', tuple[Node, Node])
# Components are represented by a forest of trees
# where the root is the canonical representative of
# of the component.
Forest = NewType('Forest', list[Node])


def root(f: Forest, v: Node) -> Node:
    """Locate the root of v's forest."""
    while f[v] != v:
        v = f[v]
    return v


def union(f: Forest, v: Node, w: Node) -> None:
    """Merge v's and w's components and update comp accordingly."""
    # Get the components of the two nodes.
    root_v, root_w = root(f, v), root(f, w)

    if root_v == root_w:
        return  # They are already in the same component

    # Make one's root point to the other. It doesn't matter
    # which (although you can get better performance if you
    # care a bit about it...)
    f[root_w] = root_v


def components(n: int, edges: list[Edge]) -> Forest:
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
    # Initially, each node has its own component
    components = Forest([Node(i) for i in range(n)])
    for v, w in edges:
        assert 0 <= v < n and 0 <= w < n
        union(components, v, w)

    return components
