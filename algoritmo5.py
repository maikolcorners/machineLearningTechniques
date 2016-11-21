# -*- coding: utf-8 -*-


import numpy as np
from sklearn import preprocessing 
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.mixture import GMM
from sklearn import metrics
import seaborn as sns
import sqlite3 as lite
import codecs
import os
import csv

filename = "data_incidencias2.db"

# def function load data
def loaddata():
	con = lite.connect('data_inicidencias2.db')
	cur = con.cursor()
	data = []
	for row in cur.execute('select zona,count(*) from incidencias group by zona'):
		data.append([row[0], row[1]])
	i=0
	for row in cur.execute('select zona,count(*) from incidencias where nivel = \'Blanco\'  group by zona'):
		for j in range(row[0]-i):
			data[i].append(0)
			i+=1
		data[i].append(row[1])
		i+=1
	for k in range(12-i):
		data[i].append(0)
		i+=1
	i=0
	for row in cur.execute('select zona,count(*) from incidencias where nivel = \'Amarillo\'  group by zona'):
		for j in range(row[0]-i):
			data[i].append(0)
			i+=1
		data[i].append(row[1])
		i+=1
	for k in range(12-i):
		data[i].append(0)
		i+=1
	i=0
	for row in cur.execute('select zona,count(*) from incidencias where nivel = \'Rojo\'  group by zona'):
		for j in range(row[0]-i):
			data[i].append(0)
			i+=1
		data[i].append(row[1])
		i+=1
	for k in range(12-i):
		data[i].append(0)
		i+=1
	i=0
	for row in cur.execute('select zona,count(*) from incidencias where nivel = \'Negro\'  group by zona'):
		for j in range(row[0]-i):
			data[i].append(0)
			i+=1
		data[i].append(row[1])
		i+=1
	for k in range(12-i):
		data[i].append(0)
		i+=1
	i=0
	for row in cur.execute('select avg(abs(pk_final-pk_inicial)) from incidencias group by zona'):
		data[i].append(row[0])
		i+=1
	return data

data=loaddata()
print (data)
with open("output.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(data)

