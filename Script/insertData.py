from GeoInfoSystem.models import *
from django.contrib.auth.models import User
#FOR INTRODUCE DATA INTO DB FIRST YOU NEED TO MAKE FLUSH COMMAND TO DELETE ALL INFO: python manage.py flush
#THEN OPEN PYSHELL: python manage.py shell
#cpy all lines and save one by one variable in database using .save() method.

punt1=puntInteres(latitud=41.29115, longitud=1.250758, idMapa=1, tipus='casa meva', actiu=True, superficie=25, localitat='Valls', pais='Catalunya')
punt2=puntInteres(latitud=41.143500, longitud=1.129970, idMapa=1, tipus='Palau de Congressos', actiu=True, superficie=20, localitat='Reus', pais='Catalunya')
punt3=puntInteres(latitud=41.132038, longitud=1.245340, idMapa=1, tipus='Universitat', actiu=True, superficie=100, localitat='Tarragona', pais='Catalunya')
punt4=puntInteres(latitud=41.297987, longitud=1.258412, idMapa=1, tipus='Restauracio', actiu=True, superficie=20, localitat='Valls', pais='Catalunya')
usuari1=User(nom='Cesc', alies="CescFT", cognom='Ferré', contrassenya='password1', correuElectronic='correu1@correu.com', superUsuari=True)
usuari2=User(nom='Toni', alies="ToniM", cognom='Martínez', contrassenya='password2', correuElectronic='correu2@correu.com', superUsuari=True)
usuari3=User(nom='usr1', alies="testUsr" , cognom='lastname1', contrassenya='password3', correuElectronic='test1@correu.com', superUsuari=False)
local1=local(localitzacio=punt1, nomLocal='Casa', puntuacio=5, categoria='casa', anyConstruccio=1995, descripcio='Molt acollidora.')
local2=local(localitzacio=punt2, nomLocal='Fira de Reus', puntuacio=5, categoria='Congressos', anyConstruccio=1990, descripcio='Interior molt xulo.')
local3=local(localitzacio=punt3, nomLocal='Campus Sescelades - Universitat Rovira i Virgili', puntuacio=4, categoria='Universitat', anyConstruccio=1985, descripcio='S\'apren molt')
local4=local(localitzacio=punt4, nomLocal='McDonald\'s', puntuacio=3, categoria='Restaurant', anyConstruccio=2019, descripcio='Es menjen coses de menjar rapid.')

punt1.save()
punt2.save()
punt3.save()
usuari1.save()
usuari2.save()
usuari3.save()
local1.save()
local2.save()
local3.save()
local4.save()
