from django.core.exceptions import FieldDoesNotExist
from django.shortcuts import render
from rest_framework import status, request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Exceptions import NoContingut
from GeoInfoSystem.models import *
from GeoInfoSystem.serializers import *
from Exceptions import *
import json
# Create your views here.
###################################################################
# API PER ALS PUNTS D'INTERÈS.                                    #
###################################################################
@api_view(['GET',])
def getPuntsInteres(request):
    if request.method == 'GET':
        try:
            puntsInteres = puntInteres.objects.all()
            if not puntsInteres:
                raise NoContingut
            serializer = puntInteresSerializer(puntsInteres, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception or NoContingut:
            return Response('No hi ha Punts d\'interès.', status=status.HTTP_404_NOT_FOUND)


@api_view(['GET',])
def getPuntInteresByCity(request):
    if request.method == 'GET':
        try:
            localitat=request.query_params.get('ciutat')
            puntsInteres = puntInteres.objects.all().filter(localitat=localitat)
            if not puntsInteres:
                raise NoContingut
            serializer = puntInteresSerializer(puntsInteres, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception or NoContingut:
            return Response('No hi ha Punts d\'interès.', status=status.HTTP_404_NOT_FOUND)
    #return Response(request.query_params.get('p'), status=status.HTTP_200_OK)

@api_view(['GET',])
def getPuntInteresEspecific(request):
    if request.method == 'GET':
        try:
            latitud=request.query_params.get('latitud')
            longitud=request.query_params.get('longitud')
            puntInteresCercat= puntInteres.objects.all().filter(latitud=latitud, longitud=longitud)
            if not puntInteresCercat:
                raise NoContingut
            serializer = puntInteresSerializer(puntInteresCercat, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception or NoContingut:
            return Response('No s\'ha trobat cap punt d\'interes en aquestes coordenades.', status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT',])
def updatePuntInteres(request, latitud, longitud):
    #per tal de fer un update real en el camp primer el que s'ha de fer es: model.objects.all().filter(filtre_per_quedarnos_amb_1).update(field1=newvalue1, field2=newvalue2, ...)
    if request.method == 'PUT':
        body_decoded=request.body.decode('utf-8')
        body=json.loads(body_decoded) #json data
        print(body) #get info --> value=body["key"]
        keys=body.keys()
        errorsInEntryJSON=""
        for key in keys:
            try:
                puntInteres._meta.get_field(key)
            except FieldDoesNotExist:
                errorsInEntryJSON=errorsInEntryJSON+'['+str(key)+"] no es un camp correcte."
        if errorsInEntryJSON:
            errorsInEntryJSON=errorsInEntryJSON+'Revisa els camps i torna executar!'
            return Response(errorsInEntryJSON, status=status.HTTP_400_BAD_REQUEST)
        try:
            puntInteresCercat = puntInteres.objects.all().filter(latitud=latitud, longitud=longitud)
            if not puntInteresCercat:
                raise NoContingut
        except Exception or NoContingut:
            return Response('No s\'ha trobat cap punt d\'interes en les coordenades ['+str(latitud)+','+str(longitud)+']', status=status.HTTP_404_NOT_FOUND)
        #No hi ha error en les dades dentrada
        latitudModificada=False
        longitudModificada=False
        novaLatitud=0.0
        novaLongitud=0.0
        for key in keys:
            if key == 'latitud':
                puntInteres.objects.all().filter(latitud=latitud, longitud=longitud).update(latitud=body[key])
                latitudModificada=True
                novaLatitud=body[key]
            elif key == 'longitud':
                puntInteres.objects.all().filter(latitud=latitud, longitud=longitud).update(longitud=body[key])
                longitudModificada=True
                novaLongitud=body[key]
            elif key == 'idMapa':
                puntInteres.objects.all().filter(latitud=latitud, longitud=longitud).update(idMapa=body[key])
            elif key == 'tipus':
                puntInteres.objects.all().filter(latitud=latitud, longitud=longitud).update(tipus=body[key])
            elif key == 'actiu':
                puntInteres.objects.all().filter(latitud=latitud, longitud=longitud).update(actiu=body[key])
            elif key == 'superficie':
                puntInteres.objects.all().filter(latitud=latitud, longitud=longitud).update(superficie=body[key])
            elif key == 'localitat':
                puntInteres.objects.all().filter(latitud=latitud, longitud=longitud).update(localitat=body[key])
            elif key == 'pais':
                puntInteres.objects.all().filter(latitud=latitud, longitud=longitud).update(pais=body[key])
            elif key == 'idPuntInteres':
                puntInteres.objects.all().filter(latitud=latitud, longitud=longitud).update(idPuntInteres=body[key])

        puntInteresCercat = puntInteres.objects.all().filter(latitud=latitud, longitud=longitud)
        if latitudModificada and longitudModificada:
            puntInteresCercat = puntInteres.objects.all().filter(latitud=novaLatitud, longitud=novaLongitud)
        elif latitudModificada and not longitudModificada:
            puntInteresCercat = puntInteres.objects.all().filter(latitud=novaLatitud, longitud=longitud)
        elif longitudModificada and not latitudModificada:
            puntInteresCercat = puntInteres.objects.all().filter(latitud=latitud, longitud=novaLongitud)


        serializer = puntInteresSerializer(puntInteresCercat, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST',])
def postNewPuntInteres():
    pass

@api_view(['DELETE',])
def deletePuntInteres(request,puntInteres):
    lol=request.query_params.get('fields')
    return Response(puntInteres+str(lol), status=status.HTTP_200_OK)

###################################################################
# API PER ALS USUARIS.                                            #
###################################################################
@api_view(['GET',])
def getUsuaris():
    pass

@api_view(['GET',])
def getUsuariEspecific():
    pass

@api_view(['PUT',])
def updateUsuari():
    pass

@api_view(['POST',])
def postNewUsuari():
    pass

@api_view(['DELETE',])
def deleteUsuari():
    pass

###################################################################
# API PER ALS Locals.                                             #
###################################################################
@api_view(['GET',])
def getLocals():
    pass

@api_view(['GET',])
def getLocalEspecific():
    pass

@api_view(['PUT',])
def updateLocal():
    pass

@api_view(['POST',])
def postNewLocal():
    pass

@api_view(['DELETE',])
def deleteLocal():
    pass



