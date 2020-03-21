import MySQLdb

datos = ['localhost', 'root', '', 'GIS_DB']
conn = MySQLdb.connect(*datos)
conn.set_character_set('utf8')
cursor = conn.cursor()
cursor.execute("SET NAMES UTF8;")

cursor.execute("SELECT id, ciutat FROM geoinfosystem_localitzacio WHERE(ciutat IN ('Valls', 'Reus', 'Tarragona'))")
myresult = cursor.fetchall()
print(myresult)
for elem in myresult:
    if elem[1] == 'Valls':
        punt1 = "INSERT INTO geoinfosystem_puntinteres (latitud, longitud, actiu, superficie, localitat_id) VALUES (41.29115, 1.250758, 1, 25, "+str(elem[0])+")"
        punt2 = "INSERT INTO geoinfosystem_puntinteres (latitud, longitud, actiu, superficie, localitat_id) VALUES (41.297987, 1.258412, 1, 50, " + str(elem[0]) + ")"
        cursor.execute(punt1) #casa meva
        conn.commit()
        cursor.execute(punt2) #Mcdonals
        conn.commit()
    if elem[1] == 'Reus':
        punt3 = "INSERT INTO geoinfosystem_puntinteres (latitud, longitud, actiu, superficie, localitat_id) VALUES (41.143500, 1.129970, 1, 20, " + str(elem[0]) + ")"
        cursor.execute(punt3) #firacongressos
        conn.commit()
    if elem[1] == 'Tarragona':
        punt4 = "INSERT INTO geoinfosystem_puntinteres (latitud, longitud, actiu, superficie, localitat_id) VALUES (41.132038, 1.245340, 1, 20, " + str(elem[0]) + ")"
        cursor.execute(punt4) # uni
        conn.commit()

