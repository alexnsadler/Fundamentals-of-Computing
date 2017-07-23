"""Algorithmic Thinking Week 4 Homework."""

# imports poc_queue
import random
import collections
import urllib
import timeit
import matplotlib.pyplot as plt


#############################################################################
# Provided Code

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """Load a graph given the URL for a text representation of the graph.

    Returns a dictionary that models a graph
    """
    graph_file = urllib.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[: -1]

    print "Loaded graph with", len(graph_lines), "nodes"

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1: -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


def copy_graph(graph):
    """Make a copy of a graph."""
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph


def delete_node(ugraph, node):
    """Delete a node from an undirected graph."""
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)


def targeted_order(ugraph):
    """Compute a targeted attack order consisting of nodes of maximal degree.

    Returns:
    A list of nodes

    """
    # copy the graph
    new_graph = copy_graph(ugraph)

    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node

        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order


class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm.

    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities

    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a complete graph.

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes)
                              for dummy_idx in range(num_nodes)]

    def run_trial(self, num_nodes):
        """Conduct num_nodes trials by applying random.choice().

        Apply random.choice() to the list of node numbers

        Updates the list of node numbers so that each node number
        appears in correct ratio

        Returns:
        Set of nodes

        """
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))

        # update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors


#############################################################################
# My Code

def bfs_visited(ugraph, start_node):
    """Return a list of visited nodes using BFS."""
    queue = collections.deque()
    visited = [start_node]
    queue.append(visited[0])

    while len(queue) != 0:
        node = queue.popleft()
        neighbors = list(ugraph[node])
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)

    return set(visited)


def cc_visited(ugraph):
    """Return a list of sets of connected components in the graph."""
    remaining_nodes = ugraph.keys()
    all_connected_comps = []

    while remaining_nodes != []:
        search_node = remaining_nodes[0]
        connected_comps = bfs_visited(ugraph, search_node)
        all_connected_comps.append(connected_comps)
        remaining_nodes = [node for node in remaining_nodes
                           if node not in connected_comps]

    return all_connected_comps


def largest_cc_size(ugraph):
    """Return the size of the largest connected component for a graph."""
    largest_size = 0
    for comp in cc_visited(ugraph):
        if len(comp) > largest_size:
            largest_size = len(comp)

    return largest_size


def compute_resilience(ugraph, attack_order):
    """Return a list of cc sizes after removing nodes from attack order."""
    size_list = [largest_cc_size(ugraph)]
    for node in attack_order:
        for edge in ugraph[node]:
            ugraph[edge] = ugraph[edge].difference(set([node]))
        ugraph.pop(node)
        size_list.append(largest_cc_size(ugraph))
    return size_list


def make_rand_undir_graph(num_nodes, prob):
    """Return a dictionary of a random, undirected graph."""
    edges_lst = []
    for nodei in range(num_nodes - 1):
        for nodej in range(nodei + 1, num_nodes):
            if prob > random.random():
                edges_lst.append((nodei, nodej))
                edges_lst.append((nodej, nodei))

    edges_lst.sort()

    graph_lst = []
    for idx in range(num_nodes):
        connections = []
        while edges_lst and edges_lst[0][0] == idx:
            node = edges_lst.pop(0)
            connections.append(node[1])

        graph_lst.append((idx, set(connections)))

    return dict(graph_lst)


def compute_num_edges(dict_list):
    """Compute the number of total edges for a graph."""
    count = 0
    for edges in dict_list.values():
        count += len(edges)
    return count / 2


def random_order(graph):
    """Generate a random order of nodes for a graph."""
    rand_list = graph.keys()
    random.shuffle(rand_list)
    return rand_list


def upa_algorithm(n_nodes, m_nodes):
    """Create a graph based on UPATrial's."""
    upa_dict = dict([(idx, set([])) for idx in range(n_nodes)])
    obj = UPATrial(1)

    for idx in range(1, n_nodes + 1):
        new_connections = obj.run_trial(m_nodes)
        upa_dict[idx] = new_connections
        for node in new_connections:
            upa_dict[node].add(idx)

    return upa_dict


def fast_target_order(ugraph):
    """Return a list of nodes in decreasing order of their degrees."""
    new_graph = copy_graph(ugraph)

    degree_sets = [(set([])) for _ in range(len(new_graph))]

    for node in (new_graph):
        degree = len(new_graph[node])
        degree_sets[degree].add(node)

    order = []

    for idx in reversed(range(len(ugraph))):
        while len(degree_sets[idx]):
            node = degree_sets[idx].pop()
            neighbors = new_graph[node]
            for neighbor in neighbors:
                neighbor_degree = len(new_graph[neighbor])
                degree_sets[neighbor_degree].remove(neighbor)
                degree_sets[neighbor_degree - 1].add(neighbor)
            order.append(node)
            delete_node(new_graph, node)

    return order


def running_times(ugraph, function, num_nodes, num_edges, step):
    """Return running time to compute the targeted order of a graph."""
    running_time = []

    for idx in range(step, num_nodes, step):
        time1 = timeit.default_timer()
        function(ugraph(idx, num_edges))
        time2 = timeit.default_timer()
        elapsed_time = time2 - time1
        running_time.append((idx, elapsed_time))

    # normally would be dict(running_time) but order changes for a dict
    return (running_time)


def question_one():
    """Generate size of largest connected comp vs number of nodes removed."""
    num_nodes, prob, m_nodes = 1239, .004, 2

    network_graph = load_graph(NETWORK_URL)
    rand_graph = make_rand_undir_graph(num_nodes, prob)
    upa_graph = upa_algorithm(num_nodes, m_nodes)

    rand_order = range(num_nodes)
    random.shuffle(rand_order)

    network_graph_resilience = compute_resilience(network_graph, rand_order)
    rand_graph_resilience = compute_resilience(rand_graph, rand_order)
    upa_graph_resilience = compute_resilience(upa_graph, rand_order)

    x_vals = range(1240)
    rand_graph_y = rand_graph_resilience
    network_graph_y = network_graph_resilience
    upa_graph_y = upa_graph_resilience

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    plt.title('Size of Largest CC vs Number of Nodes Removed')
    plt.xlabel('Numbe of Nodes Removed')
    plt.ylabel('Size of Largest CC')

    ax1.plot(x_vals, rand_graph_y, label="ER Graph, p = .004")
    ax1.plot(x_vals, network_graph_y, label="Network Graph")
    ax1.plot(x_vals, upa_graph_y, label="UPA Graph, m = 2")

    ax1.legend(loc='upper right')

    plt.show()


def question_three():
    """Generate a graph for running time v number of nodes for target order."""
    targeted_order_times = running_times(upa_algorithm, targeted_order,
                                         1000, 5, 10)
    fast_target_order_times = running_times(upa_algorithm, fast_target_order,
                                            1000, 5, 10)

    q3_x_vals = [idx[0] for idx in fast_target_order_times]
    to_times_y = [idx[1] for idx in targeted_order_times]
    fto_times_y = [idx[1] for idx in fast_target_order_times]

    fig = plt.figure()
    ax2 = fig.add_subplot(111)

    plt.title('Desktop Implementation of Running Times vs Number of Nodes')
    plt.xlabel('Number of Nodes, m = 5')
    plt.ylabel('Running Time (Seconds)')

    ax2.plot(q3_x_vals, to_times_y, label="targeted_order")
    ax2.plot(q3_x_vals, fto_times_y, label="fast_target_order")

    ax2.legend(loc='upper right')

    plt.show()


def question_four():
    """Generate a graph of largest CC vs targeted number of nodes removed."""
    num_nodes, prob, m_nodes = 1239, .004, 2

    network_graph = load_graph(NETWORK_URL)
    rand_graph = make_rand_undir_graph(num_nodes, prob)
    upa_graph = upa_algorithm(num_nodes, m_nodes)

    network_target_resilience = compute_resilience(network_graph, fast_target_order(network_graph))
    rand_target_resilience = compute_resilience(rand_graph, fast_target_order(rand_graph))
    upa_target_resilience = compute_resilience(upa_graph, fast_target_order(upa_graph))

    q4_xvals = range(1240)
    rand_target_y = rand_target_resilience
    network_target_y = network_target_resilience
    upa_target_y = upa_target_resilience

    print len(rand_target_y)
    print len(network_target_y)
    print len(upa_target_y)

    fig = plt.figure()
    ax3 = fig.add_subplot(111)

    plt.title('Size of Largest CC vs Targeted Number of Nodes Removed')
    plt.xlabel('Numbe of Nodes Removed')
    plt.ylabel('Size of Largest CC')

    ax3.plot(q4_xvals, rand_target_y, label="ER Graph, p = .004")
    ax3.plot(q4_xvals, network_target_y, label="Network Graph")
    ax3.plot(q4_xvals, upa_target_y, label="UPA Graph, m = 2")

    ax3.legend(loc='upper right')
    plt.show()
