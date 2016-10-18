# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 08:32:57 2016

@author: FranciscoP.Romero
"""

import sqlite3 as lite
import codecs
import os
import matplotlib.pyplot as plt
import sklearn.neighbors
import numpy as np


# def function load data 
def loaddata(filename):
	dbfile = filename
	con = lite.connect(dbfile)
	cur = con.cursor()
	data = []
	for row in cur.execute('SELECT longitud,latitud FROM incidencias'):
		data.append([float(row[0]), float(row[1])])
	return data

def plotdata(data,labels,name): #def function plotdata
#colors = ['black']
    fig, ax = plt.subplots()
    plt.scatter([row[0] for row in data], [row[1] for row in data], c=labels)
    ax.grid(True)
    fig.tight_layout()
    plt.title(name)
    plt.show()


# 0. load and plot data (datos.csv)
data = loaddata("data_inicidencias2.db")
labels = [0 for x in range(len(data))]
plotdata(data,labels,'basic')


# 1. setting parameters
# 1.1 Compute the similarity/distance matrix (high cost)
# The graphic could offer better results (improve it!!)
dist = sklearn.neighbors.DistanceMetric.get_metric('euclidean')
matsim = dist.pairwise(data)
# 1.2 Compute the k-nearest neighboors
minPts=10
from sklearn.neighbors import kneighbors_graph
A = kneighbors_graph(data, minPts, include_self=False)
Ar = A.toarray()

seq = []
for i,s in enumerate(data):
    for j in range(len(data)):
        if Ar[i][j] != 0:
            seq.append(matsim[i][j])
            
seq.sort()
plt.plot(seq)
plt.show()

# 2. Execute clustering (dbscan)
import sklearn.cluster
labels = sklearn.cluster.DBSCAN(eps=0.08, min_samples=minPts).fit_predict(data)

# 3. Plot the results
plotdata(data,labels, 'dbscan')

# 4. Validation
from sklearn import metrics
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(np.asarray(data), labels))

                       
                       
