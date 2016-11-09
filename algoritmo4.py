# -*- coding: utf-8 -*-

# cargar datos y primer gráfico sin clustering.

import sqlite3 as lite
import codecs
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics


# def function load data
def loaddata(con):
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


#Connection
con = lite.connect("data_inicidencias2.db")
#load and plot data
data = loaddata(con)
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

#add a new field in db about zone
###con.execute('ALTER TABLE INCIDENCIAS ADD zona INT')
cur = con.cursor()
for i in range(len(labels)):
	cur.execute('UPDATE INCIDENCIAS SET zona=' + str(labels [i]) + ' WHERE id=' + str(i))
con.commit()
