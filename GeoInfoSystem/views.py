from django.shortcuts import render
from rest_framework import status, request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Exceptions import NoContingut
from GeoInfoSystem.models import *
from GeoInfoSystem.serializers import *
from Exceptions import *

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
def getPuntInteresEspecific(request, id):
    pass

@api_view(['PUT',])
def updatePuntInteres():
    pass

@api_view(['POST',])
def postNewPuntInteres():
    pass

@api_view(['DELETE',])
def deletePuntInteres():
    pass

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



