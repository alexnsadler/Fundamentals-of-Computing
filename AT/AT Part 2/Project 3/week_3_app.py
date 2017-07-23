"""Project 3 application (student written)."""

import random
import timeit
import alg_cluster
import alg_project3_solution as des
import matplotlib.pyplot as plt


def gen_random_clusters(num_clusters):
    """Return a list of randomly generated points in the corners of a square.

    Input: num_clusters is the number of desired random clusters

    Output: List of tuples that have possible values of (+/- 1, +/- 1)
    """
    cluster_list = []
    point_values = (-1, 1)
    for idx in range(num_clusters):
        h_cord = random.choice(point_values)
        v_cord = random.choice(point_values)
        cluster = alg_cluster.Cluster(set(), h_cord, v_cord, 0, 0)
        cluster_list.append(cluster)
    return cluster_list


def running_times(num_clusters, function):
    """Return a list of running times for num_clusters for a given function.

    Input: num_clusters is the number of clusters, and function is either
    fast_closest_pair or slow_closest_pair from alg_project3_solution

    Output: list of running times
    """
    times_list = []
    for num_cluster in range(2, num_clusters):
        cluster_lst = gen_random_clusters(num_cluster)

        start_time = timeit.default_timer()
        function(cluster_lst)
        stop_time = timeit.default_timer()

        elapsed_time = stop_time - start_time
        times_list.append(elapsed_time)
    return times_list


def compute_distortion(cluster_list, data_url):
    """Compute the distorition of a cluster_list.

    Uses cluster_error from alg_cluster to compute the error of each cluster
    (the sum of the sequares of distances from each county in the cluster to
    the cluster's center, weighted by each county's population)

    Input: cluster_list is a list of clusters

    Output: the distortion of a cluster_list
    """
    # Change argument for load_data_table depending on cluster_list input
    data_table = des.load_data(data_url)

    distortion = 0
    for cluster in cluster_list:
        distortion += cluster.cluster_error(data_table)

    return distortion


def clustering_distortion(data_url, cluster_method):
    """Return a list of distortions.

    Input: a data_url for information on cancer data and either clustering
    method of des.kmeans_clustering or des.hierarchical_clustering

    Output: a list of distortions for a range of iterations for
    kmeans_clustering
    """
    cluster_list = des.cluster_lst(data_url)
    distortions_list = []

    if cluster_method == des.kmeans_clustering:
        for num_clstr in range(6, 21):
            kmeans_clusters = des.kmeans_clustering(cluster_list, num_clstr, 5)
            distortions_list.append(compute_distortion(kmeans_clusters, data_url))

    elif cluster_method == des.hierarchical_clustering:
        init_hierachical_clusters = des.hierarchical_clustering(cluster_list, 20)
        distortions_list.append(compute_distortion(init_hierachical_clusters, data_url))
        for num_clstr in range(19, 5, -1):
            hierachical_clusters = des.hierarchical_clustering(init_hierachical_clusters, num_clstr)
            distortions_list.append(compute_distortion(hierachical_clusters, data_url))
        distortions_list.reverse()

    else:
        return "Invalid cluster_method"

    return distortions_list
###############################################################################
# Application answers


def question_one():
    """Generate graph of running time of pair functions for 200 clusters."""
    q1_x_vals = range(2, 200)
    slow_vals = running_times(200, des.slow_closest_pair)
    fast_vals = running_times(200, des.fast_closest_pair)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    plt.title('Running Time of Pair Functions for 200 Clusters in Desktop Python')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Running Time in Seconds')

    ax1.plot(q1_x_vals, slow_vals, label="slow_closest_pair")
    ax1.plot(q1_x_vals, fast_vals, label="fast_closest_pair")

    ax1.legend(loc='upper right')

    plt.show()


# Answers for questions 2, 3, 5, and 6 are in alg_project3_viz


def question_seven():
    """Return the distortion for kmeans and hierarchical clusters."""
    q7_data_url = des.DATA_111_URL  # change url depending on desired data table
    q7_clst = des.cluster_lst(q7_data_url)
    q7_kmeans_clusters = des.kmeans_clustering(q7_clst, 9, 5)
    q7_hierarchical_clusters = des.hierarchical_clustering(q7_clst, 9)

    kmeans_dist = compute_distortion(q7_kmeans_clusters, q7_data_url)
    hierarchical_dist = compute_distortion(q7_hierarchical_clusters, q7_data_url)

    return "hierarchical distortion =", hierarchical_dist, "kmeans distortion =", kmeans_dist


def question_ten():
    """Generate graph for distortions vsn umber of clusters."""
    kmeans_dist_111 = clustering_distortion(des.DATA_111_URL,
                                            des.kmeans_clustering)
    kmeans_dist_290 = clustering_distortion(des.DATA_290_URL,
                                            des.kmeans_clustering)
    kmeans_dist_896 = clustering_distortion(des.DATA_896_URL,
                                            des.kmeans_clustering)

    hierarchical_dist_111 = clustering_distortion(des.DATA_111_URL,
                                                  des.hierarchical_clustering)
    hierarchical_dist_290 = clustering_distortion(des.DATA_290_URL,
                                                  des.hierarchical_clustering)
    hierarchical_dist_896 = clustering_distortion(des.DATA_896_URL,
                                                  des.hierarchical_clustering)

    q2_x_vals = range(6, 21)
    # change the below values for desired graph/ number of points
    kmeans_vals = kmeans_dist_896
    hierarchical_vals = hierarchical_dist_896
    num_points = 896

    fig = plt.figure()
    ax2 = fig.add_subplot(111)

    plt.title('Disortions vs Number of Clusters for ' + str(num_points) + ' points')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Distortions * 10^11')

    ax2.plot(q2_x_vals, kmeans_vals, label="kmeans_clustering")
    ax2.plot(q2_x_vals, hierarchical_vals, label="hierarchical_clustering")

    ax2.legend(loc='upper right')

    plt.show()
