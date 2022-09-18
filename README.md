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

You can generate all roads leading out of city `A`, but it involves keeping track of the current path, which neighbours we have explored and which we haven’t, and backtracking when we reach a dead end, so I will not do that. I will do something simpler and just explore all cities we can reach without worrying about whether I see them in any order that matches a roadtrip. If we do it that way, we only need to keep track of which cities we have seen and which cities we have processed.

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

Let's say that `0` is now picked from `unprocessed`. This won't add any new neigbours, of coures--`1` is its only neighbour and we already have that in `seen`--so nothing much happens.

![Exploration 4](figs/comp/simple-graph-explore%203.png)

The next node to be popped from `unprocessed` has to be `4` (it is the only one there), and that will add `3` and `5`.

![Exploration 5](figs/comp/simple-graph-explore%204.png)

I will stop here, as I am confident that you can finish the example on your own.

Notice how we have a growing set of `seen` nodes as we move `unprocessed` as a form of border of this set, expanding through the graph. When `unprocessed` is eventually empty, we have seen everything we can reach from the initial node, and we return that.

Of course, if you already know that you are searching for a specific node, you can terminate early; if you see it in the exploration, you know that you can reach it.

