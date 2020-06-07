import MySQLdb
import mysql.connector as mariadb
import csv

tarragona={}
barcelona={}
lleida={}
girona={}

print('Municipis de Tarragona')
f = open('../municipis/municipis_tarragona.txt', 'r', encoding='utf-8')
lines = f.readlines()
i=1
for line in lines:
    if line.split('\t')[1]!='\n':
        tarragona['poble'+str(i)] = line.split('\t')[0].replace('\'','\\\'')+","+line.split('\t')[1].replace('\n', '').replace('\'','\\\'')
        i= i + 1
print(tarragona)
datos = ['localhost', 'root', '', 'GIS_DB']
conn = MySQLdb.connect(*datos)
conn.set_character_set('utf8')
cursor = conn.cursor()
cursor.execute("SET NAMES UTF8;")
#ALTER TABLE geoinfosystem_localitzacio CONVERT TO CHARACTER SET utf8;
#mariadb_connection = mariadb.connect(user='root', password='', database='GIS_DB', charset='utf8', use_unicode=True)
#cursor = mariadb_connection.cursor()
for key in tarragona:
    nomCiutat = tarragona[key].split(',')[0]
    nomComarca = tarragona[key].split(',')[1]
    cursor.execute("INSERT INTO geoinfosystem_localitzacio (ciutat, comarca, provincia) VALUES ('"+nomCiutat+"', '"+nomComarca+"', 'Tarragona');")
    #mariadb_connection.commit()
    conn.commit()

print('Municipis de Barcelona')
f = open('../municipis/municipis_barcelona.txt', 'r', encoding='utf-8')
lines = f.readlines()
i=1
for line in lines:
    if line.split('\t')[1]!='\n':
        barcelona['poble'+str(i)] = line.split('\t')[0].replace('\'','\\\'')+","+line.split('\t')[1].replace('\n', '').replace('\'','\\\'')
        i= i + 1
print(barcelona)
datos = ['localhost', 'root', '', 'GIS_DB']
conn = MySQLdb.connect(*datos)
conn.set_character_set('utf8')
cursor = conn.cursor()
cursor.execute("SET NAMES UTF8;")
#ALTER TABLE geoinfosystem_localitzacio CONVERT TO CHARACTER SET utf8;
#mariadb_connection = mariadb.connect(user='root', password='', database='GIS_DB', charset='utf8', use_unicode=True)
#cursor = mariadb_connection.cursor()
for key in barcelona:
    nomCiutat = barcelona[key].split(',')[0]
    nomComarca = barcelona[key].split(',')[1]
    cursor.execute("INSERT INTO geoinfosystem_localitzacio (ciutat, comarca, provincia) VALUES ('"+nomCiutat+"', '"+nomComarca+"', 'Barcelona');")
    #mariadb_connection.commit()
    conn.commit()

print('Municipis de Lleida')
f = open('../municipis/municipis_lleida.txt', 'r', encoding='utf-8')
lines = f.readlines()
i=1
for line in lines:
    if line.split('\t')[1]!='\n':
        lleida['poble'+str(i)] = line.split('\t')[0].replace('\'','\\\'')+","+line.split('\t')[1].replace('\n', '').replace('\'','\\\'')
        i= i + 1
print(lleida)
datos = ['localhost', 'root', '', 'GIS_DB']
conn = MySQLdb.connect(*datos)
conn.set_character_set('utf8')
cursor = conn.cursor()
cursor.execute("SET NAMES UTF8;")
#ALTER TABLE geoinfosystem_localitzacio CONVERT TO CHARACTER SET utf8;
#mariadb_connection = mariadb.connect(user='root', password='', database='GIS_DB', charset='utf8', use_unicode=True)
#cursor = mariadb_connection.cursor()
for key in lleida:
    nomCiutat = lleida[key].split(',')[0]
    nomComarca = lleida[key].split(',')[1]
    cursor.execute("INSERT INTO geoinfosystem_localitzacio (ciutat, comarca, provincia) VALUES ('"+nomCiutat+"', '"+nomComarca+"', 'Lleida');")
    #mariadb_connection.commit()
    conn.commit()

print('Municipis de Girona')
f = open('../municipis/municipis_girona.txt', 'r', encoding='utf-8')
lines = f.readlines()
i=1
for line in lines:
    if line.split('\t')[1]!='\n':
        girona['poble'+str(i)] = line.split('\t')[0].replace('\'','\\\'')+","+line.split('\t')[1].replace('\n', '').replace('\'','\\\'')
        i= i + 1
print(girona)
datos = ['localhost', 'root', '', 'GIS_DB']
conn = MySQLdb.connect(*datos)
conn.set_character_set('utf8')
cursor = conn.cursor()
cursor.execute("SET NAMES UTF8;")
#ALTER TABLE geoinfosystem_localitzacio CONVERT TO CHARACTER SET utf8;
#mariadb_connection = mariadb.connect(user='root', password='', database='GIS_DB', charset='utf8', use_unicode=True)
#cursor = mariadb_connection.cursor()
for key in girona:
    nomCiutat = girona[key].split(',')[0]
    nomComarca = girona[key].split(',')[1]
    cursor.execute("INSERT INTO geoinfosystem_localitzacio (ciutat, comarca, provincia) VALUES ('"+nomCiutat+"', '"+nomComarca+"', 'Girona');")
    #mariadb_connection.commit()
    conn.commit()
