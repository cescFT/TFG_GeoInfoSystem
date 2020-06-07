import MySQLdb

datos = ['localhost', 'root', '', 'GIS_DB']
conn = MySQLdb.connect(*datos)
conn.set_character_set('utf8')
cursor = conn.cursor()
cursor.execute("SET NAMES UTF8;")

cursor.execute("INSERT INTO geoinfosystem_categoriaLocal (categoria) VALUES ('Restauració')") #""" 'RESTAURACIO', 'CULTURA', 'HABITATGE'"""
conn.commit()
cursor.execute("INSERT INTO geoinfosystem_categoriaLocal (categoria) VALUES ('Cultura')")
conn.commit()
cursor.execute("INSERT INTO geoinfosystem_categoriaLocal (categoria) VALUES ('Habitatge')")
conn.commit()
cursor.execute("INSERT INTO geoinfosystem_categoriaLocal (categoria) VALUES ('Congrés')")
conn.commit()
cursor.execute("INSERT INTO geoinfosystem_categoriaLocal (categoria) VALUES ('Universitat')")
conn.commit()