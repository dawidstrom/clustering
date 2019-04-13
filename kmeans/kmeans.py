from PIL import Image
from functools import reduce
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import time
import sys
import random as rnd
import math


def euclidean(point0, point1):
    """
    Simply calculates the euclidean distance between two points in any
    dimension.

    point0: D-dimensional tuple of first points location.
    point1: D-dimensional tuple of second points location.
    """
    return math.sqrt(sum(map(lambda x: math.pow(abs(x[0]-x[1]),2), zip(point0, point1))))


def kmeans(datapoints, k, N=10):
    """
    Classifies datapoints into k number of clusters using Loyd's algorithm.

    Args
    datapoints: List of datapoints. Each datapoint can be a single value or a
                tuple of values.
    k: Number of clusters to classify datapoints into.
    N: Number of iterations to calculate clusters.
    """

    centers = []
    clusters = []
    no_repicks = list(set(datapoints))
    
    # Pick k random datapoints.
    for i in range(k):
        item = rnd.choice(no_repicks)
        centers.append(item)
        no_repicks.remove(item)


    # Repeat N number of times.
    for i in range(N):
        clusters.clear();
        for a in range(k):
            clusters.append([]) # Reset cluster classification.

        # Group datapoints into its respective cluster.
        for p_index in range(len(datapoints)):
            # The default infinitly bad cluster.
            closest = (0, math.inf)

            # Compute euclidean distance to each cluster center.
            for c_index in range(len(centers)):
                dist = euclidean(centers[c_index], datapoints[p_index])
                if (dist < closest[1]):
                    closest = (c_index, dist)

            # Add point and point index to its cluster.
            clusters[closest[0]].append((p_index, datapoints[p_index]))

        # Make new cluster center by taking mean of points in cluster.
        for c_index in range(len(centers)):
            cluster = clusters[c_index] # Get cluster.
            cc = [x[1] for x in cluster] # Extract color information remain.
            # Elementwise sum of color.
            mean = reduce(lambda s,x: (s[0]+x[0],s[1]+x[1],s[2]+x[2]), cc)
            # Get average for each element.
            mean = ( int(mean[0]/len(cc)), int(mean[1]/len(cc)), int(mean[2]/len(cc)) )
            centers[c_index] = mean # Update cluster center.

        print("Iteration {%i} complete." % (i))
    
    
    flat_ordered = [0] * len(datapoints)

    # Order cluster points in same order as datapoints.
    for c_index in range(len(clusters)):
        # Set cluster points to have center color.
        for point in clusters[c_index]:
            flat_ordered[point[0]] = centers[c_index]

    #plot(clusters)
    return flat_ordered


def plot(clusters):
    """
    Plot datapoints into 3D space and colors each point according to which
    cluster it belongs to.

    Args
    clusters: List where each index is a list of points (3d tuples) in that 
    cluster.
    """

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for c_index in range(len(clusters)):
        x = [x[0] for x in clusters[c_index]]
        y = [y[1] for y in clusters[c_index]]
        z = [z[2] for z in clusters[c_index]]
        ax.scatter3D(x,y,z,z,cmap='Greens')
    plt.show()


def print_help():
    """
    Prints command usage.
    """
    print("Usage: python kmeans.py image.[jpg,png,etc] [k] [iterations]")


if __name__ == '__main__':
    # Determine if the correct number of parameters were given.
    if (len(sys.argv) < 2 or len(sys.argv) > 4):
        print_help();
        sys.exit(1)

    iterations = 1
    k = 3

    if len(sys.argv) >= 3:
        k = int(sys.argv[2])
    if len(sys.argv) == 4:
        iterations = int(sys.argv[3])

    # Load data.
    im = Image.open(sys.argv[1])
    datapoints = list(im.getdata())
    clustered_data = kmeans(datapoints, k, iterations);

    # Construct image from clusters.
    img = Image.new(im.mode, im.size)

    # Order datapoints based on 
    im.putdata(clustered_data)
    im.show()
