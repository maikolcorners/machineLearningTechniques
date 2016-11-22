# -*- coding: utf-8 -*-

import codecs
import matplotlib.pyplot as plt
import numpy
from sklearn.decomposition import PCA
from sklearn import preprocessing 
import sklearn.cluster

# 0. Load Data
f = codecs.open("output.csv", "r", "utf-8")
zones = []
for line in f:
	row = line.replace ('"', '').split(",")
	row.pop(0)
	if row != []:
		data = [float(el) for el in row]
		zones.append(row)

#1. Normalization of the data
min_max_scaler = preprocessing.MinMaxScaler()
zones = min_max_scaler.fit_transform(zones)
print zones
        
#2. PCA Estimation
estimator = PCA (n_components = 2)
X_pca = estimator.fit_transform(zones)
print X_pca

#3.  plot 
numbers = numpy.arange(len(X_pca))
fig, ax = plt.subplots()

for i in range(len(X_pca)):
    plt.text(X_pca[i][0], X_pca[i][1], numbers[i]) 
  
plt.xlim(-2.2, 0.7)
plt.ylim(-0.6, 1)
ax.grid(True)
fig.tight_layout()
plt.show()

