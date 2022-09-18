# Connecting grap-nodes, connected components and union-find

This note considers a simple graph where we have `n` nodes, indexed as integers `0, 1, ..., n - 1`, and we have a list of undirected edges `(i,j)` that should be interpreted as there being a connection between node `i` and node `j` and vice versa. The question we consider is an example from *Computational Thinking in Bioinformatics* where we ask whether it is possible to get from one node `A` to another, `B` (framed as cities with roads between them).

There are many ways to solve this problem, but we will only consider two. The one that I had in mind when posing the question that uses connected components of a graph and another solution that came up in class, where we explore all the roads out of `A` to see if we can get to `B`. According to Matthew 20:16, the first shall be the last, so we consider the second solution first.

## Exploring all cities we can reach from `A`

With this approach, we want to explore all roads leading out of `A` exhaustively. To do this, we will first have to order our edges in a way such that we can easily get the immediate neighbours of any node, but luckily this is easy if we make a list of sets for them.

We can construct a list of length `n` consisting of empty sets and then run through the edges `(v,w)` adding `w` as `v`’s neighbour and `v` as `w`’s neighbour.

```python
def build_neighbours(n, edges):
    """Collect sets of neighbours for each node."""
    neighbours = [set() for _ in range(n)]
    for v, w in edges:
        neighbours[v].add(w)
        neighbours[w].add(v)
    return neighbours
```

If we had the simple graph below,

![Simple graph](figs/comp/simple-graph.png)

running this function should give us:

```python
>>> build_neighbours(5, [(0, 1), (2, 1), (3, 4)])
[{1}, {0, 2}, {1}, {4}, {3}]
```

You can generate all roads leading out of city `A`, but it involves keeping track of the current path, which neighbours we have explored and which we haven’t, and backtracking when we reach a dead end, so I will not do that. I will do something more straightforward and just explore all cities we can reach without worrying about whether I see them in any order that matches a road trip. If we do it that way, we only need to keep track of which cities we have seen and which we have processed.

```python
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
```

Let's take the function for a spin. Consider the graph below, and imagine that we start the exploration from node `1`. I won't write the sets on the figure, but mark nodes in `seen` with an `s` and nodes in `unprocessed` with a `u`. Initially, we have `1` in both sets.

![Exploration 1](figs/comp/simple-graph-explore.png)

The only node we can take out of `unprocessed` is `1`, so we do that, remove it from `unprocessed` (but not `seen`) and add its neighbours to both sets.

![Exploration 2](figs/comp/simple-graph-explore%201.png)

The `pop()` method on sets picks an arbirary element, so we don't really know which one it will be, but let us imagine that it is `2`. That means that `2` is removed from `unexplored` but that its neighbour, `4`, is added to both sets.

![Exploration 3](figs/comp/simple-graph-explore%202.png)

Let's say that `0` is now picked from `unprocessed`. This won't add any new neighbours, of course—`1` is its only neighbour, and we already have that in `seen`—so nothing much happens.

![Exploration 4](figs/comp/simple-graph-explore%203.png)

The next node to be popped from `unprocessed` has to be `4` (it is the only one there), which will add `3` and `5`.

![Exploration 5](figs/comp/simple-graph-explore%204.png)

I will stop here as I am confident that you can finish the example on your own.

Notice how we have a growing set of `seen` nodes as we move `unprocessed` as a form of border of this set, expanding through the graph. When `unprocessed` is eventually empty, we have seen everything we can reach from the initial node, and we return that.

Of course, if you already know that you are searching for a specific node, you can terminate early; if you see it in the exploration, you know you can reach it.

## Building connected components

A connected component in a graph is a maximal set of nodes that can all reach each other. Maximal, here, means that there are no nodes outside the set that can reach all the nodes inside it.

If we run the function we wrote above, we get a set of all the nodes we can reach from a given one, and since you can travel in both directions along all the edges in this note, all nodes in this set can reach each other—it is a connected component.

We can solve the problem of determining if `A` can reach `B` by asking if `A` and `B` are in the same component. That is essentially what we did above. There, we built `A`’s component by exhaustively traversing the graph, but below I will show you a different method of doing the same thing and in a way such that we get *all* the connected components at the same time.

We will use a trick called [*union-find* or *disjoint set*](https://en.wikipedia.org/wiki/Disjoint-set_data_structure), but the basic idea is not as fancy as that sounds.

But before we get clever, we will implement the idea in a simpler and slower way.

### Simple component structure

We need a way to represent components, and for that, we can use something as simple as a list. Let’s call it `comp`. We will loop through all the edges, and the invariant we will have the following invariant:

**Invariant:** For each node `v`, we use `comp[v]` as a representative for `v`’s node, according to the edges we have seen so far.

What we mean by “representative” is anything that uniquely identifies the component, in the sense that `comp[v] == comp[w]` if and only if `v` and `w` are in the same component.

For our first attempt, we will initialise `comp` as `comp[v] = v`; that is, for each node `v`, `comp[v]` contains the node itself. This is clearly a unique representative since no two components are the same, and it represents the components before we have seen any edge at all since, with no edges, each node is its own component.

In the figure below, I have shown a graph on the left. There are three edges, but I have drawn them in dotted grey to indicate that we haven't processed them yet.

![Initial component](figs/comp/initial-components.png)

On the top right is the `comp` array, initialised to `comp[v] = v`. Below I have a slightly different representation, where each node points to its component representative (i.e. itself).

Now what we will do is loop through all edges `(v, w)`. When we process `(v, w)`, we need to join `comp[v]` and `comp[w]`. We can pick one or the other representative as the new representative, it doesn't matter which. Without loss of generality, let's say we choose to move all elements in `w`'s component to component `comp[v]`. This means that for all nodes `u` with `comp[u] == comp[w]` (all nodes in the same component as `w`) we must change the component to `comp[u] = comp[v]`.

A simple way to handle that is to run through the components and update all nodes with component `comp[w]` like this:

```python
def union(comp: list[int], v: int, w: int) -> None:
    """Merge v's and w's components and update comp accordingly."""
    cv, cw = comp[v], comp[w]
    for u, cu in enumerate(comp):
        if cu == cw:
            comp[u] = cv
```

It isn't super efficient, since we have to look at the components for all nodes each time we join two components, but it gets the job done.[^1]

[^1]: You can of course return before the loop if `cv == cw`, and that would be a good optimisation, but it doesn't change the worst case running time, so to keep the code simple I have left that out.

