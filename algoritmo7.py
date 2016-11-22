#!/usr/bin/env python
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import numpy
import codecs
from scipy import cluster
from sklearn import preprocessing 
import sklearn.neighbors

# 0. Load Data

f = codecs.open("output.csv", "r", "utf-8")
zones = []
for line in f: 
	row = line.replace ('"', '').split(",")
	row.pop(0)
	if row != []:
		zones.append(map(float, row))
 
 
#1. Normalization of the data
min_max_scaler = preprocessing.MinMaxScaler()
zones = min_max_scaler.fit_transform(zones)
	
# 2. Compute the similarity matrix
dist = sklearn.neighbors.DistanceMetric.get_metric('euclidean')
matsim = dist.pairwise(zones)
avSim = numpy.average(matsim)
print "%s\t%6.2f" % ('Distancia Media', avSim)

# 3. Building the Dendrogram	
clusters = cluster.hierarchy.linkage(matsim, method = 'ward')
cluster.hierarchy.dendrogram(clusters, color_threshold=0)
plt.show()


# 4. Cutting the dendrogram
#Forms flat clusters from the hierarchical clustering defined by the linkage matrix clusters
# introduce the value after dendrogram visualization
cut = float(input("Threshold cut:"))
clusters = cluster.hierarchy.fcluster(clusters, cut , criterion = 'distance')
print 'Number of clusters %d' % (len(set(clusters)))

