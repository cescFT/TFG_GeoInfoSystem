"""
Classe que permet retornar la informació en format JSON de tot el que hi ha en el model de dades.
"""
from rest_framework import serializers
from . models import *

class puntInteresSerializer(serializers.ModelSerializer):
    class Meta:
        model=puntInteres
        fields='__all__'

class usuariSerializer(serializers.ModelSerializer):
    class Meta:
        model=usuari
        fields='__all__'
        
class localSerializer(serializers.ModelSerializer):
    class Meta:
        model=local
        fields='__all__'