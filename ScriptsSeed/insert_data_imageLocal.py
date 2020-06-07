import MySQLdb

datos = ['localhost', 'root', '', 'GIS_DB']
conn = MySQLdb.connect(*datos)
conn.set_character_set('utf8')
cursor = conn.cursor()
cursor.execute("SET NAMES UTF8;")

cursor.execute("SELECT id FROM geoinfosystem_local WHERE(nomLocal =\"Casa\")")
casaID = cursor.fetchone()[0]
imageCasa='CasaMevaRedim.jpg'
cursor.execute("INSERT INTO geoinfosystem_imagelocal (imatge, local_id) VALUES ('"+imageCasa+"',"+str(casaID)+")")
conn.commit()
cursor.execute("SELECT id FROM geoinfosystem_local WHERE(nomLocal =\"Fira de Reus\")")
firadereusID = cursor.fetchone()[0]
imageFiraReus = 'firaReusRedim.jpg'
cursor.execute("INSERT INTO geoinfosystem_imagelocal (imatge, local_id) VALUES ('"+imageFiraReus+"',"+str(firadereusID)+")")
conn.commit()
cursor.execute("SELECT id FROM geoinfosystem_local WHERE(nomLocal =\"McDonals\")")
McDonaldsID = cursor.fetchone()[0]
imagemcdonals= 'mcdonaldsVallsRedim.jpg'
cursor.execute("INSERT INTO geoinfosystem_imagelocal (imatge, local_id) VALUES ('"+imagemcdonals+"',"+str(McDonaldsID)+")")
conn.commit()
cursor.execute("SELECT id FROM geoinfosystem_local WHERE(nomLocal =\"Campus Sescelades - Universitat Rovira i Virgili\")")
urv = cursor.fetchone()[0]
imageurvcampusseselades = 'urvCampusSesceladesRedim.jpg'
cursor.execute("INSERT INTO geoinfosystem_imagelocal (imatge, local_id) VALUES ('"+imageurvcampusseselades+"',"+str(urv)+")")
conn.commit()

'''
cursor.execute("SELECT id FROM geoinfosystem_puntinteres WHERE(latitud=41.29115 AND longitud=1.250758)")
casa = cursor.fetchone()[0]

cursor.execute("SELECT id FROM geoinfosystem_puntinteres WHERE(latitud=41.297987 AND longitud=1.258412)")
mcdonalds = cursor.fetchone()[0]

cursor.execute("SELECT id FROM geoinfosystem_puntinteres WHERE(latitud=41.1435 AND longitud=1.12997)")
firacongressos = cursor.fetchone()[0]

cursor.execute("SELECT id FROM geoinfosystem_categoriaLocal WHERE (categoria='Habitatge')")
categoria_casa = cursor.fetchone()[0]

cursor.execute("SELECT id FROM geoinfosystem_categoriaLocal WHERE (categoria='Restauracio')")
categoria_restauracio = cursor.fetchone()[0]

cursor.execute("SELECT id FROM geoinfosystem_categoriaLocal WHERE (categoria='Congrés')")
categoria_congres = cursor.fetchone()[0]

cursor.execute("SELECT id FROM geoinfosystem_categoriaLocal WHERE (categoria='Universitat')")
categoria_universitat = cursor.fetchone()[0]

cursor.execute("INSERT INTO geoinfosystem_local (nomLocal, estat_conservacio, categoria_id, localitzacio_id, anyConstruccio, descripcio) VALUES ('Casa', 5, "+str(categoria_casa)+","+str(casa)+", 1995, 'Molt acollidora.')")
conn.commit()

cursor.execute("INSERT INTO geoinfosystem_local (nomLocal, estat_conservacio, categoria_id, localitzacio_id, anyConstruccio, descripcio) VALUES ('Fira de Reus', 5, "+str(categoria_congres)+","+str(firacongressos)+", 1990, 'Interior molt xulo.')")
conn.commit()

cursor.execute("INSERT INTO geoinfosystem_local (nomLocal, estat_conservacio, categoria_id, localitzacio_id, anyConstruccio, descripcio) VALUES ('Campus Sescelades - Universitat Rovira i Virgili', 4, "+str(categoria_universitat)+","+str(universitat)+",1985,'Lloc on el coneixement és important.')")
conn.commit()

cursor.execute("INSERT INTO geoinfosystem_local (nomLocal, estat_conservacio, categoria_id, localitzacio_id, anyConstruccio, descripcio) VALUES ('McDonals', 3, "+str(categoria_restauracio)+","+str(mcdonalds)+", 2019, 'Es menjen coses de menjar rapid.')")
conn.commit()
'''