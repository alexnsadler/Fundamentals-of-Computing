"""
Student template code for Project 3.

Student will implement five functions:
slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import urllib
import alg_cluster

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"


def load_data(datafile):
    """Load cancer risk data from .csv file."""
    data_file = urllib.urlopen(datafile)
    data = data_file.read()
    data_lines = data.split('\n')
    # print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]),
            float(tokens[4])] for tokens in data_tokens]


def cluster_lst(data_info):
    """Return a list of Cluster objects."""
    data = load_data(data_info)

    data_lst = []
    for idx in range(len(data)):
        data_lst.append(alg_cluster.Cluster(set([data[idx][0]]), data[idx][1],
                        data[idx][2], data[idx][3], data[idx][4]))

    return data_lst


######################################################
# All student written code below
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Compute Euclidean distance for two clusters in a list (helper function).

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices
    for two clusters

    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2),
            max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow).

    Input: cluster_list is the list of clusters

    Output: tuple of the form (dist, idx1, idx2) where the centers of the
    clusters cluster_list[idx1] and cluster_list[idx2]
    have minimum distance dist.
    """
    min_dist, idx_i, idx_j = 'inf', -1, -1

    for idx1 in range(len(cluster_list)):
        for idx2 in range(len(cluster_list)):
            if cluster_list[idx1].distance(cluster_list[idx2]) < min_dist:
                if cluster_list[idx1].distance(cluster_list[idx2]) != 0:
                    min_dist = float(cluster_list[idx1].distance(cluster_list[idx2]))
                    idx_i = idx1
                    idx_j = idx2

    return (min_dist, idx_i, idx_j)


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Compute the closest pair of clusters in a vertical strip.

    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal
    distance that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the
    clusters cluster_list[idx1] and cluster_list[idx2] lie in the strip and
    have minimum distance dist.
    """
    index_lst = [(idx, cluster_list[idx]) for idx in range(len(cluster_list))
                 if abs(cluster_list[idx].horiz_center() - horiz_center)
                 < half_width]
    index_lst.sort(key=lambda cluster: cluster[1].vert_center())

    len_list = len(index_lst)
    min_val = (float('inf'), -1, -1)

    for idx1 in range(len_list - 1):
        for idx2 in range(idx1 + 1, min(idx1 + 4, len_list)):
            current_d = pair_distance(cluster_list, index_lst[idx1][0],
                                      index_lst[idx2][0])
            if current_d < min_val:
                min_val = current_d

    return min_val


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast).

    Input: cluster_list is list of clusters SORTED such that horizontal
    positions of their centers are in ascending order

    Output: tuple of the form (dist, idx1, idx2) where the centers of the
    clusters cluster_list[idx1] and cluster_list[idx2] have min distance dist.
    """
    lst_length = len(cluster_list)

    if lst_length <= 3:
        min_val = slow_closest_pair(cluster_list)
    else:
        middle = lst_length / 2
        lst_left = cluster_list[: middle]
        lst_right = cluster_list[middle: lst_length]

        dist_l = fast_closest_pair(lst_left)
        dist_r = fast_closest_pair(lst_right)

        if dist_r <= dist_l:
            min_val = (dist_r[0], dist_r[1] + middle, dist_r[2] + middle)
        else:
            min_val = dist_l

        mid_x = .5 * (cluster_list[middle - 1].horiz_center() +
                      cluster_list[middle].horiz_center())
        strip_list = closest_pair_strip(cluster_list, mid_x, min_val[0])

        if strip_list <= min_val:
            min_val = strip_list

    return min_val


######################################################################
# Code for hierarchical clustering

def hierarchical_clustering(cluster_list, num_clusters):
    """Compute a hierarchical clustering of a set of clusters.

    Note: the function may mutate cluster_list

    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        cluster_list.sort(key=lambda cluster: cluster.horiz_center())

        closest_pair = fast_closest_pair(cluster_list)
        cluster_1 = cluster_list[closest_pair[1]]
        cluster_2 = cluster_list[closest_pair[2]]

        cluster_1.merge_clusters(cluster_2)
        cluster_list.pop(closest_pair[2])

    return cluster_list


######################################################################
# Code for k-means clustering

def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """Compute the k-means clustering of a set of clusters.

    Note: the function may not mutate cluster_list

    Input: List of clusters, integers num of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    # position initial clusters at the location of clusters with largest pops.
    cluster_copy = list(cluster_list)

    cluster_copy.sort(key=lambda cluster: cluster.total_population(),
                      reverse=True)

    centers_list = []
    for idx in range(num_clusters):
        centers_list.append((cluster_copy[idx].horiz_center(),
                             cluster_copy[idx].vert_center()))

    for _ in range(num_iterations):
        empty_clusters = [alg_cluster.Cluster(set(),
                          centers_list[idx][0],
                          centers_list[idx][1], 0, 0.0)
                          for idx in range(num_clusters)]

        new_clusters = [alg_cluster.Cluster(set(),
                        centers_list[idx][0],
                        centers_list[idx][1], 0, 0.0)
                        for idx in range(num_clusters)]

        for idx2 in range(len(cluster_list)):
            min_val = float('inf')
            for idx3 in range(num_clusters):
                cur_dist = empty_clusters[idx3].distance(cluster_copy[idx2])
                if cur_dist < min_val:
                    min_val = cur_dist
                    cluster_2 = idx3
            new_clusters[cluster_2].merge_clusters(cluster_copy[idx2])

        # update centers
        for idx4 in range(num_clusters):
            centers_list[idx4] = (new_clusters[idx4].horiz_center(),
                                  new_clusters[idx4].vert_center())

    return new_clusters
