from django.db import models
# Create your models here.

"""
Classe que representarà el punt en el mapa. Les altres informacion són per si es necessiten més tard al clicar al punt.
"""
class puntInteres(models.Model):
    latitud=models.FloatField()
    longitud=models.FloatField()
    idMapa=models.IntegerField()
    tipus=models.CharField(max_length=700)
    actiu=models.BooleanField()
    superficie=models.FloatField()
    localitat=models.CharField(max_length=200)
    pais=models.CharField(max_length=200)
    idPuntInteres=models.IntegerField()
    def __str__(self):
        return "Punt interes localitzat:["+str(self.latitud)+","+str(self.longitud)+"] actiu="+str(self.actiu)+"de tipus:"+str(self.tipus)

"""
Classe referent als usuaris que estaran presents en el sistema. (<<PROVISIONAL>>)
"""
class usuari(models.Model):
    nom=models.CharField(max_length=500)
    alies=models.CharField(max_length=500)
    cognom=models.CharField(max_length=500)
    contrassenya=models.CharField(max_length=500)
    correuElectronic=models.EmailField()
    superUsuari=models.BooleanField()
    def __str__(self):
        return self.nom

"""
Classe que serà el que donarà la informació del element que hi ha en el punt d'interès específic. 
En cas que el punt d'interès s'elimini, també s'esborrarà el local, en conseqüència, ja que sinó el sistema quedaria 
incosistent.
"""
class local(models.Model):
    localitzacio=models.ForeignKey(puntInteres, on_delete=models.CASCADE)
    nomLocal=models.CharField(max_length=500)
    puntuacio=models.IntegerField()
    categoria=models.CharField(max_length=200)
    anyConstruccio=models.IntegerField()
    descripcio=models.CharField(max_length=600)
    idLocal=models.IntegerField()
    def __str__(self):
        return str(self.nomLocal)+" puntuacio="+str(self.puntuacio)+" categoria="+str(self.categoria)+" any construccio="+str(self.anyConstruccio)


