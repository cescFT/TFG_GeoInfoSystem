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
    def __str__(self):
        return "{"+"latitud:\"" + str(self.latitud) + "\", longitud:\"" + str(self.longitud) + "\", idMapa:\"" + str(self.idMapa) + "\", tipus:\"" + str(self.tipus) + "\", actiu:\"" + str(self.actiu)+ "\", superficie:\"" + str(self.superficie) + "\", localitat:\"" + str(self.localitat) + "\", pais:\"" + str(self.pais)+"\""+"}";


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
    def __str__(self):
        return "{"+"nomLocal:\"" + str(self.nomLocal) + "\", puntuacio:\"" + str(self.puntuacio) + "\", categoria:\"" + str(self.categoria) + "\", anyConstruccio:\"" + str(self.anyConstruccio) + "\", descripcio:\"" + str(self.descripcio)+ "\", superficie:\""+"}";


