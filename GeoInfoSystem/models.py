from django.db import models
# Create your models here.

class puntInteres(models.Model):
    latitud=models.FloatField()
    logitud=models.FloatField()
    idMapa=models.IntegerField()
    tipus=models.CharField(max_length=700)
    actiu=models.BooleanField()
    superficie=models.FloatField()
    localitat=models.CharField(max_length=200)
    pais=models.CharField(max_length=200)

class usuari(models.Model):
    nom=models.CharField(max_length=500)
    cognom=models.CharField(max_length=500)
    contrassenya=models.CharField(max_length=500)
    correuElectronic=models.EmailField()
    superUsuari=models.BooleanField()

class local(models.Model):
    localitzacio=models.ForeignKey(puntInteres, on_delete=models.CASCADE)
    nomLocal=models.CharField(max_length=500)
    puntuacio=models.IntegerField()
    categoria=models.CharField(max_length=200)
    anyConstruccio=models.IntegerField()
    descripcio=models.CharField(max_length=600)


