from django.db import models
# Create your models here.

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

class usuari(models.Model):
    nom=models.CharField(max_length=500)
    alies=models.CharField(max_length=500)
    cognom=models.CharField(max_length=500)
    contrassenya=models.CharField(max_length=500)
    correuElectronic=models.EmailField()
    superUsuari=models.BooleanField()
    def __str__(self):
        return self.nom

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


