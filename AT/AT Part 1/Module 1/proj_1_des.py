"""Algorithmic Thinking Project One Assignment."""

EX_GRAPH0 = {0: set([1, 2]),
             1: set([]),
             2: set([])}

EX_GRAPH1 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3]),
             3: set([0]),
             4: set([1]),
             5: set([2]),
             6: set([])}

EX_GRAPH2 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3, 7]),
             3: set([7]),
             4: set([1]),
             5: set([2]),
             6: set([]),
             7: set([3]),
             8: set([1, 2]),
             9: set([0, 4, 5, 6, 7, 3])}


def make_complete_graph(num_nodes):
    """Return a dictionary for a directed complete graph."""
    lst = []
    for node in range(num_nodes):
        dict_val = [idx for idx in range(num_nodes) if idx != node]
        lst.append((node, set(dict_val)))
    return dict(lst)


def compute_in_degrees(digraph):
    """Return a dictionary with the number of in-degree nodes for each node."""
    in_deg_list = []
    for node in digraph:
        node_deg = 0
        for val in digraph.values():
            if node in val:
                node_deg += 1
        in_deg_list.append((node, node_deg))

    return dict(in_deg_list)


def in_degree_distribution(digraph):
    """Return the distribution of in-degrees for the given graph."""
    deg_val_lst = compute_in_degrees(digraph).values()

    deg_dst = []
    for idx in range(len(deg_val_lst)):
        in_deg_count = deg_val_lst.count(idx)
        if in_deg_count != 0:
            deg_dst.append((idx, in_deg_count))

    return dict(deg_dst)
