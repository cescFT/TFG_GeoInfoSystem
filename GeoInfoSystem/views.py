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
import re
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
        body=json.loads(body_decoded) #json data #get info --> value=body["key"]
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
                if body[key] == 'True' or body[key] == 1:
                    actiu=True
                else:
                    actiu=False
                puntInteres.objects.all().filter(latitud=latitud, longitud=longitud).update(actiu=actiu)
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
def postNewPuntInteres(request):
    if request.method == 'POST':
        body_decoded = request.body.decode('utf-8')
        body = json.loads(body_decoded)  # json data #get info --> value=body["key"]
        keys = body.keys()
        errorsInEntryJSON = ""
        for key in keys:
            try:
                puntInteres._meta.get_field(key)
            except FieldDoesNotExist:
                errorsInEntryJSON = errorsInEntryJSON + '[' + str(key) + "] no es un camp correcte."
        if errorsInEntryJSON:
            errorsInEntryJSON = errorsInEntryJSON + 'Revisa els camps i torna executar!'
            return Response(errorsInEntryJSON, status=status.HTTP_400_BAD_REQUEST)
        latitud=0.0
        longitud=0.0
        idMapa=1
        tipus=""
        actiu=False
        superficie=0.0
        localitat=""
        pais=""
        idPuntInteres=100
        for key in keys:
            if key == 'latitud':
                latitud=body[key]
            elif key == 'longitud':
                longitud=body[key]
            elif key == 'idMapa':
                idMapa=body[key]
            elif key == 'tipus':
                tipus=body[key]
            elif key == 'actiu':
                if body[key] == 1 or body[key] == 'True':
                    actiu=True
                else:
                    actiu=False
            elif key == 'superficie':
                superficie=body[key]
            elif key == 'localitat':
                localitat=body[key]
            elif key == 'pais':
                pais=body[key]
            elif key == 'idPuntInteres':
                idPuntInteres=body[key]
        pInteresCercat=puntInteres.objects.all().filter(latitud=latitud, longitud=longitud)
        if not pInteresCercat:
            pInteresNou=puntInteres(latitud=latitud, longitud=longitud, idMapa=idMapa, tipus=tipus, actiu=actiu, superficie=superficie, localitat=localitat, pais=pais, idPuntInteres=idPuntInteres)
            pInteresNou.save()
            pINou=puntInteres.objects.all().filter(latitud=latitud, longitud=longitud)
            serializer = puntInteresSerializer(pINou, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            #return Response('creariem un nou punt interes')
        else:
            return Response(puntInteresSerializer(pInteresCercat, many=True).data, status=status.HTTP_200_OK)
            #return Response('rebotariem el que estava ja')

@api_view(['DELETE',])
def deletePuntInteres(request):
    if request.method == 'DELETE':
        latitud=request.query_params.get('latitud')
        longitud=request.query_params.get('longitud')
        if not latitud or not longitud:
            return Response('Falten parametres per a poder eliminar la instancia', status=status.HTTP_400_BAD_REQUEST)
        try:
            p=puntInteres.objects.all().filter(latitud=latitud, longitud=longitud)
            if not p:
                raise NoContingut
        except Exception or NoContingut:
            return Response('No hi ha cap punt d\'interes amb aquestes coordenades.', status=status.HTTP_404_NOT_FOUND)
        puntInteres.objects.all().filter(latitud=latitud, longitud=longitud).delete()
        return Response('Punt d\'interes eliminat correctament.', status=status.HTTP_200_OK)

###################################################################
# API PER ALS USUARIS.                                            #
###################################################################
@api_view(['GET',])
def getUsuaris(request):
    if request.method == 'GET':
        try:
            usuaris = usuari.objects.all()
            if not usuaris:
                raise NoContingut
            serializer = usuariSerializer(usuaris, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception or NoContingut:
            return Response('No hi ha usuaris.', status=status.HTTP_404_NOT_FOUND)

@api_view(['GET',])
def getSuperUsuaris(request):
    if request.method=='GET':
        try:
            superusuaris=usuari.objects.all().filter(superUsuari=True)
            if not superusuaris:
                raise NoContingut
            serializer = usuariSerializer(superusuaris, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception or NoContingut:
            return Response('No hi ha superusuaris.', status=status.HTTP_404_NOT_FOUND)

@api_view(['GET',])
def getUsuarisNormals(request):
    if request.method == 'GET':
        try:
            usuarisNormals = usuari.objects.all().filter(superUsuari=False)
            if not usuarisNormals:
                raise NoContingut
            serializer = usuariSerializer(usuarisNormals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception or NoContingut:
            return Response('No hi ha usuaris normals.', status=status.HTTP_404_NOT_FOUND)

@api_view(['GET',])
def getUsuariEspecific(request, alias):
    if request.method == 'GET':
        try:
            usuariEspecific=usuari.objects.all().filter(alies=alias)
            if not usuariEspecific:
                raise NoContingut
            serializer = usuariSerializer(usuariEspecific, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception or NoContingut:
            return Response('No existeix aquest usuari', status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT',])
def updateUsuari(request):
    if request.method == 'PUT':
        body_decoded = request.body.decode('utf-8')
        body=json.loads(body_decoded)
        keys=body.keys()
        errorsInEntryJSON=""
        for key in keys:
            try:
                usuari._meta.get_field(key)
            except FieldDoesNotExist:
                errorsInEntryJSON=errorsInEntryJSON+'['+key+']'+ 'no es un camp correcte.'
        if errorsInEntryJSON:
            errorsInEntryJSON=errorsInEntryJSON+' Revisa els camps i torna a executar!'
            return Response(errorsInEntryJSON, status=status.HTTP_400_BAD_REQUEST)
        alies=request.query_params.get('alies')
        if not alies:
            return Response('Falta el alies.', status=status.HTTP_400_BAD_REQUEST)
        try:
            usrEspecific=usuari.objects.all().filter(alies=alies)
            if not usrEspecific:
                raise NoContingut
        except Exception or NoContingut:
            return Response('No hi ha cap usuari amb aquest àlies. S\'aborta la actualització', status=status.HTTP_400_BAD_REQUEST)


        aliasChanged = False
        nouAlies =""
        for key in keys:
            if key == 'nom':
                usuari.objects.all().filter(alies=alies).update(nom=body[key])
            elif key == 'alies':
                aliasChanged=True
                nouAlies=body[key]
                usuari.objects.all().filter(alies=alies).update(alies=body[key])
            elif key == 'cognom':
                usuari.objects.all().filter(alies=alies).update(cognom=body[key])
            elif key == 'contrassenya':
                usuari.objects.all().filter(alies=alies).update(contrassenya=body[key])
            elif key == 'correuElectronic':
                regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
                if re.search(regex, body[key]):
                    usuari.objects.all().filter(alies=alies).update(correuElectronic=body[key])
            elif key == 'superUsuari':
                if body[key] == 'True' or body[key] == 1:
                    superusr=True
                else:
                    superusr=False
                usuari.objects.all().filter(alies=alies).update(superUsuari=superusr)

        #modificacions fetes
        usuariCercat = usuari.objects.all().filter(alies=alies)
        if aliasChanged:
            usuariCercat=usuari.objects.all().filter(alies=nouAlies)

        serializer = usuariSerializer(usuariCercat, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST',])
def postNewUsuari(request):
    if request.method == 'POST':
        body_decoded = request.body.decode('utf-8')
        body = json.loads(body_decoded)
        keys=body.keys()
        errorsInEntryJSON = ""
        for key in keys:
            try:
                usuari._meta.get_field(key)
            except FieldDoesNotExist:
                errorsInEntryJSON = errorsInEntryJSON + '[' + str(key) + "] no es un camp correcte."
        if errorsInEntryJSON:
            errorsInEntryJSON = errorsInEntryJSON + 'Revisa els camps i torna executar!'
            return Response(errorsInEntryJSON, status=status.HTTP_400_BAD_REQUEST)
        nom=""
        alies=""
        cognom=""
        contrassenya=""
        correuElectronic="initialMail@mail.com"
        superUsuari=False
        for key in keys:
            if key == 'nom':
                nom=body[key]
            elif key == 'alies':
                alies=body[key]
            elif key == 'cognom':
                cognom=body[key]
            elif key == 'contrassenya':
                contrassenya=body[key]
            elif key == 'correuElectronic':
                regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
                if re.search(regex, body[key]):
                    correuElectronic=body[key]
            elif key == 'superUsuari':
                if body[key] == 'True' or body[key] == 1:
                    superUsuari=True
        usuariSpec = usuari.objects.all().filter(alies=alies)
        if not usuariSpec:
            newUsr = usuari(nom=nom, alies=alies, cognom=cognom, contrassenya=contrassenya, correuElectronic=correuElectronic, superUsuari=superUsuari)
            newUsr.save()
            newUsrCercat = usuari.objects.all().filter(alies=alies)
            serializer = usuariSerializer(newUsrCercat, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE',])
def deleteUsuari(request, alias):           #no provat. sha de provar
    if request.method=='DELETE':
        if not alias:
            return Response('Falta el alies per a poder eliminar la instancia.', status=status.HTTP_400_BAD_REQUEST)
        try:
            usuariCercat = usuari.objects.all().filter(alies=alias)
            if not usuariCercat:
                raise NoContingut
        except Exception or NoContingut:
            return Response('No hi ha cap usuari amb aquest alies.', status=status.HTTP_404_NOT_FOUND)
        usuari.objects.all().filter(alies=alias).delete()
        return Response('Usuari eliminat correctament.', status=status.HTTP_200_OK)

###################################################################
# API PER ALS Locals.                                             #
###################################################################
@api_view(['GET',])
def getLocals(request):
    if request.method == 'GET':
        try:
            locals = local.object.all()
            if not locals:
                raise NoContingut
            serializer = localSerializer(locals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception or NoContingut:
            return Response('No hi ha locals.', status=status.HTTP_404_NOT_FOUND)

@api_view(['GET',])
def getLocalEspecificByLatLong(request, latitud, longitud):
    if request.method == 'GET':
        if not latitud or not longitud:
            return Response('Falten els parametres per a poder executar la operacio.', status=status.HTTP_400_BAD_REQUEST)
        try:
            punt1=puntInteres.objects.all().filter(latitud=latitud, longitud=longitud)
            if not punt1:
                raise NoContingut
            localCercat = local.objects.all().filter(localitzacio=punt1)
            if not localCercat:
                raise NoContingut
            return Response(localSerializer(localCercat, many=True).data, status=status.HTTP_200_OK)
        except Exception or NoContingut:
            return Response('No hi ha cap local en aquestes coordenades.', status=status.HTTP_404_NOT_FOUND)
@api_view(['GET',])
def getLocalEspecificByName(request, nomLocal):
    if request.method == 'GET':
        if not nomLocal:
            return Response('Falta el parametre per a poder executar la operacio.', status=status.HTTP_400_BAD_REQUEST)
        try:
            localCercat=local.objects.all().filter(nomLocal=nomLocal)
            if not localCercat:
                raise NoContingut
            return Response(localSerializer(localCercat, many=True).data, status=status.HTTP_200_OK)
        except Exception or NoContingut:
            return Response('No hi ha cap local amb aquest nom.', status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT',])
def updateLocalByLatLong(request, latitud, longitud):
    if request.method == 'PUT':
        if not latitud or not longitud:
            return Response('Falten els parametres per a executar la operacio d\'actualització del local.', status=status.HTTP_400_BAD_REQUEST)
        body_decoded = request.body.decode('utf-8')
        body = json.loads(body_decoded)
        keys = body.keys()
        errorsInEntryJSON = ""
        for key in keys:
            try:
                local._meta.get_field(key)
            except FieldDoesNotExist:
                errorsInEntryJSON = errorsInEntryJSON + '[' + str(key) + "] no es un camp correcte."
        if errorsInEntryJSON:
            errorsInEntryJSON = errorsInEntryJSON + 'Revisa els camps i torna executar!'
            return Response(errorsInEntryJSON, status=status.HTTP_400_BAD_REQUEST)
        try:
            puntInteresCercat = puntInteres.objects.all().filter(latitud=latitud, longitud=longitud)
            if not puntInteresCercat:
                raise NoContingut
            localCercat=local.objects.all().filter(localitzacio=puntInteresCercat)
            if not localCercat:
                raise NoContingut
        except Exception or NoContingut:
            return Response('No hi ha cap local en aquestes coordenades.', status=status.HTTP_404_NOT_FOUND)
        # No hi ha error en les dades dentrada
        

@api_view(['PUT',])
def updateLocalByName(request, name):
    pass

@api_view(['POST',])
def postNewLocal():
    pass

@api_view(['DELETE',])
def deleteLocal():
    pass



