from django.conf.urls import url
from django.urls import path

from GeoInfoSystem import views

urlpatterns = [
    #API PUNT INTERES
    path('allPuntsInteres/', views.getPuntsInteres, name='TotsPuntsInteres'),
    path('puntInteresByCity/', views.getPuntInteresByCity, name='pInteresCiutat'),
    path('puntInteresByCoordenades/', views.getPuntInteresEspecific, name='pInteresCoordenades'),
    url(r'updatePuntInteres/(?P<latitud>\d+\.\d+)/(?P<longitud>\d+\.\d+)/$', views.updatePuntInteres, name='pInteresUpdate'),
    path('newPuntInteres/', views.postNewPuntInteres, name='pInteresCreate'),
    path('eliminarPuntInteres/', views.deletePuntInteres, name='pInteresEliminat'),
    # API USUARIS
    path('getUsuaris/', views.getUsuaris, name='usuaris'),
    path('getSuperUsuaris/', views.getSuperUsuaris, name='superUsuaris'),
    path('getUsuarisNormals/', views.getUsuarisNormals, name='usuaris Normals'),
    path('getUsuari/<str:alias>/', views.getUsuariEspecific, name='usuari'),
    path('updateUsuari/', views.updateUsuari, name='updateUsuari'),
    path('createUsuari/', views.postNewUsuari, name='createNewUsuari'),
    path('deleteUsuari/<str:alias>/', views.deleteUsuari, name='deleteUsuari')
]