"""
Classe que permet retornar la informació en format JSON de tot el que hi ha en el model de dades.
"""
from rest_framework import serializers
from . models import *
from django.contrib.auth.models import User

class puntInteresSerializer(serializers.ModelSerializer):
    class Meta:
        model=puntInteres
        fields='__all__' #per que no surti tot i nomes surti lo q a mi mintressa mostrar --> fields=('field1', 'field2', ...)


class localSerializer(serializers.ModelSerializer):
    class Meta:
        model=local
        fields='__all__'


class UserSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    is_superuser=serializers.BooleanField()

    def create(self, validated_data):
        instance = User()
        instance.first_name=validated_data.get('first_name')
        instance.last_name=validated_data.get('last_name')
        instance.username=validated_data.get('username')
        instance.email=validated_data.get('email')
        instance.set_password(validated_data.get('password'))
        instance.is_superuser = validated_data.get('is_superuser')
        instance.save()
        return instance

    def validate_username(self, data):
        users = User.objects.filter(username=data)
        if users:
           raise serializers.ValidationError("Existeix aquest nom d'usuari. Introdueix un altre nom.")
        else:
            return data
