"""
Building connected components using simple union-find operations.

Each update runs in O(n) so with O(m) edges the total running time is O(nm).
"""

from typing import NewType

# The following is just for annotating the code to keep track of the
# kind of objects we are working with. It does not affect the function
# of any of the functions.

# Nodes are represented as integers.
Node = NewType('Node', int)
# Edges are pairs of nodes.
Edge = NewType('Edge', tuple[Node, Node])
# Components are represented by a (canonical) representative
# which is a specific node from that component.
Components = NewType('Components', list[Node])


def union(comp: Components, v: Node, w: Node) -> None:
    """Merge v's and w's components and update comp accordingly."""
    # Get the components of the two nodes.
    cv, cw = comp[v], comp[w]

    if cv == cw:
        return  # They are already in the same component

    # Flip so we have the smallest in v (to avoid duplication)
    if cw < cv:
        cv, cw = cw, cv
    # Set move all the nodes in the larger component to the larger
    for i, c in enumerate(comp):
        if c == cw:
            comp[i] = cv


def components(n: int, edges: list[Edge]) -> Components:
    """
    Compute connected components.

    Compute the connected components for n nodes based on the
    edges. All the nodes listed in the edges must be values in
    the range 0 <= ... < n.

    >>> comp = components(5, [(0, 1), (2, 1), (3, 4)])
    >>> assert comp[0] == comp[1] and comp[1] == comp[2]
    >>> assert comp[3] == comp[4]
    >>> assert comp[0] != comp[3]
    """
    # Initially, each node has its own component
    components = Components([Node(i) for i in range(n)])
    for v, w in edges:
        assert 0 <= v < n and 0 <= w < n
        union(components, v, w)

    return components
