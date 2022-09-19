"""
Building connected components using a tree representation.

We contract paths when we look for roots. This can be proven to
have an amortised running time of O(log* n) so the whole
algorithm runs in O(m log* n). The log* n (iterated logarithm)
function grows incredibly slow and will never reach higher than
5 in this universe, so in practise we use O(m).

(You can actually prove that it runs in O(mׁ*a(n)) where a(n)
is the inverse Ackermann function, which is even slower than log*
but the proof is more involved and it hardly matters for anyone
ever...)
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
    # Locate the root by running up the path
    root = v
    while is_node(f[root]):
        root = f[root]

    # Then contract the path to point to the root
    while v != root:
        v, f[v] = f[v], root

    return root


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


print(components(5, [(0, 1), (2, 1), (3, 4)]))
