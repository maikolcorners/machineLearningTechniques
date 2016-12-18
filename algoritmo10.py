import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets
import random
import sqlite3 as lite

def loaddata(con, works):

	select = ''
	if (works):
		select= 'SELECT longitud,latitud FROM incidencias'
	else:
		select= 'SELECT longitud,latitud, zona FROM incidencias'
	cur = con.cursor()
	data = []
	for row in cur.execute(select):
		if (works):
			data.append([float(row[0]), float(row[1])])
		else:
			data.append([float(row[0]), float(row[1]), int(row[2])])
	return data


#Connection and load data from accidents:

con = lite.connect("data_inicidencias2.db")
data = loaddata(con, False)

#Split data:

trainingData=[]
testData=[]

for d in data:
	if random.random()<0.6:
		trainingData.append(d)
	else:
		testData.append(d)

#Training:

x=[]
y=[]

for td in trainingData:
	x.append([td[0],td[1]])
	y.append(td[2])

#Test:

x2=[]
y2=[]

for td in testData:
	x2.append([td[0],td[1]])
	y2.append(td[2])

#Get k:

bestK=-1
bestWeight=''
oldEqual=0
for weights in ['uniform', 'distance']:
	for k in range(1,50):
		clf = neighbors.KNeighborsClassifier(k, weights=weights)
		clf.fit(x, y)
		tdY = clf.predict(x2)
		i=0
		equal=0
		for aux in tdY:
			if aux==y2[i]:
				equal+=1
			i+=1
		if equal>oldEqual:
			oldEqual=equal
			bestK=k
			bestWeight=weights

#Connection and load data from works:

con = lite.connect("data_inicidencias3.db")
data = loaddata(con, True)
xWorks=[]
for d in data:
	xWorks.append([d[0],d[1]])
clf = neighbors.KNeighborsClassifier(bestK, bestWeight)
clf.fit(x,y)
zone = clf.predict(xWorks)

#Alter table and plot results:

###con.execute('ALTER TABLE INCIDENCIAS ADD zona INT')
cur = con.cursor()
for i in range(len(zone)):
	cur.execute('UPDATE INCIDENCIAS SET zona=' + str(zone [i]) + ' WHERE id=' + str(i))
con.commit()
print ('The best k value is: ' + str(bestK) + ', and best weight is: '+ str(bestWeight) + ' ' + str(oldEqual))
plt.plot(zone)
plt.xlabel('Works')
plt.ylabel('Assigned zones')
fig1 = plt.gcf()
plt.show()
fig1.savefig('Zones.png', dpi=200)
