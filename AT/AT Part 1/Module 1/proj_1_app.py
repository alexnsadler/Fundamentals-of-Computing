"""Provided and student written code for Application portion of Module 1."""

import urllib
import matplotlib.pyplot as plt
import random
import proj_1_des as des

#############################################################################
# Provided Code

DATA_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"


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


citation_graph = load_graph(DATA_URL)


class DPATrial:
    """Encapsulate optimized trials for DPA algorithm.

    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities

    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """Initialize a DPATrial object.

        DPATrial corresponding to a complete graph with num_nodes nodes

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes)
                              for dummy_idx in range(num_nodes)]

    def run_trial(self, num_nodes):
        """Conduct num_node trials using by applying random.choice().

        Apply random.choice to the list of node numbers

        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities

        Returns: Set of nodes
        """
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))

        # update the number of nodes
        self._num_nodes += 1

        return new_node_neighbors


#############################################################################
# Student written code

def make_complete_random_graph(num_nodes, prob):
    """Return a dictionary for a directed graph, based on the given prob."""
    lst = []
    # Creates a list for all possible edges between all nodes
    for node in range(num_nodes):
        dict_val = [idx for idx in range(num_nodes) if idx != node]
        lst.append((node, (dict_val)))

    new_lst = []
    for poss_nodes in lst:
        node_vals = []
        for idx in poss_nodes[1]:  # Looks at the connected nodes for each node
            if random.random() < prob:
                node_vals.append(idx)
        new_lst.append((poss_nodes[0], set(node_vals)))

    return dict(new_lst)


def compute_out_degrees(digraph):
    """Return a dict with the number of out-degree nodes for each node."""
    out_deg_list = []
    for key in digraph.keys():
        count = 0
        for val in digraph[key]:
            count += 1
        out_deg_list.append((key, count))

    return dict(out_deg_list)


def normalized_in_degree_distribution(digraph):
    """Return a normalized distriubtion from a given in_degree_distribution."""
    dist_dict = des.in_degree_distribution(digraph)
    keys = dist_dict.keys()
    denom = sum(dist_dict.values())
    vals_lst = [(idx, (float(dist_dict[idx]) / denom)) for idx in keys]
    
    return dict(vals_lst)


def question_one():
    """Generate graph of log dist percentages vs log dist of bins."""
    normalized_dist_list = normalized_in_degree_distribution(citation_graph)
    # Delete the 0 key, as log(0) doesn't evaluate
    normalized_dist_list.pop(0) 
    
    x_vals = normalized_dist_list.keys()
    y_vals = normalized_dist_list.values()

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.set_xscale('log')
    ax1.set_yscale('log')

    plt.title('Log of Distribution Percentages vs Log of Distribution Bins')
    plt.xlabel('Log of Number of Citations')
    plt.ylabel('Log of Distribution Percentages')

    ax1.scatter(x_vals, y_vals)

    plt.show()


def question_two():
    """Generate graph of normal distribution of in degrees for an ER graph."""
    q2_graph = make_complete_random_graph(1000, .5)
    q2_dict = des.in_degree_distribution(q2_graph)

    fig = plt.figure()
    ax2 = fig.add_subplot(111)

    q2_x = q2_dict.keys()
    q2_y = q2_dict.values()

    plt.title("Normal Distribution of In Degrees for ER graph")
    plt.xlabel("Number of Edges")
    plt.ylabel("Frequency of Occurence")

    ax2.scatter(q2_x, q2_y)

    plt.show()


def question_three():
    """Return the number of edges and number of nodes for the DPA graph."""
    num_edges = 352768 / 27770
    num_nodes = 27770

    return num_edges, num_nodes


def question_four():
    """Generate a graph for log freq vs log number of in degrees for DPA."""
    num_edges = question_three()[0]
    obj = DPATrial(num_edges)

    # Run run_trial from DPATrial class to add nodes and edges
    # Range should actually be n (27770) but changed for speed
    dict_lst = []
    for idx in range(10000):
        dict_lst.append((num_edges, obj.run_trial(13)))
        num_edges += 1

    q4_dict = normalized_in_degree_distribution(dict(dict_lst))
    del q4_dict[0]

    fig = plt.figure()
    ax4 = fig.add_subplot(111)

    q4_x = q4_dict.keys()
    q4_y = q4_dict.values()

    ax4.set_xscale('log')
    ax4.set_yscale('log')

    plt.title('Log Frequency vs Log Number of In Degrees for DPA Graph')
    plt.xlabel("Log of Number of In Degrees")
    plt.ylabel("Log Frequency")

    ax4.scatter(q4_x, q4_y)

    plt.show()
