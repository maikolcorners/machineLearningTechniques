#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import codecs
import os

def loaddata(con, archive, insert):
	cursor= con.cursor()
	f = codecs.open(archive, "r", "ISO-8859-1")
	count = 0
	count1= 0
	row=[]	
	for line in f:
		linea1=line.find('<?xml')		
		if linea1==-1 :
			if count > 1 and count < 17:				
				if line.find('</incidenciaGeolocalizada>')!=-1:					
					if row[2]=='ARABA':
						cursor.execute(insert, row)			
					
					row=[]
					count=0;					
				else:					
					inicio=line.find('>')
					final=line.find('</')
					row.append(line[inicio+1:final])
			elif count ==17:
				break
		
			count+=1
			
			
	cursor.close()
	con.commit()

def main():
	dbfile = 'data_inicidencias.db'
	if os.path.exists(dbfile): 
		os.remove(dbfile)
	con = lite.connect(dbfile)
	# 1. CREATE TABLES. It is possible to create the table using a SQLite Manager or SQLite command line
	# data as int because is a format YYMMDD
	con.execute('CREATE TABLE INCIDENCIAS (tipo TEXT, autonomia TEXT, provincia TEXT, matricula TEXT,'+
			'causa TEXT, poblacion TEXT, fechahora_ini TEXT, nivel TEXT, carretera TEXT,'+
			'pk_inicial INT, pk_final INT, sentido TEXT, longitud REAL, latitud REAL)')
	con.commit()

	# 2. LOAD DATA
	loaddata(con, "inc2006.xml", 
		"INSERT INTO INCIDENCIAS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
	
	
	return 0

if __name__ == '__main__':
	main()

