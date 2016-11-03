# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 08:32:57 2016

@author: FranciscoP.Romero
"""

# cargar datos y primer gráfico sin clustering.

import sqlite3 as lite
import codecs
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics


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


#load and plot data
data = loaddata("data_inicidencias2.db")
#c,data = loadtraffic()
labels = [0 for x in range(len(data))]
plotdata(data,labels,'basic')
#k-means
import sklearn.cluster
      
from sklearn import cluster      
spectral = cluster.SpectralClustering(n_clusters=12, eigen_solver='arpack', affinity="nearest_neighbors")
labels = spectral.fit_predict(data)
plotdata(data,labels,'spectral')
print("Silhouette Coefficient (Spectral): %0.3f"
      % metrics.silhouette_score(np.asarray(data), labels))
                      
                       
