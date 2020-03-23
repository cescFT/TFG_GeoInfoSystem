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
    path('deleteUsuari/<str:alias>/', views.deleteUsuari, name='deleteUsuari'),
    # API LOCALS
    path('getLocals/', views.getLocals, name='allLocals'),
    url(r'getLocalByLatLong/(?P<latitud>\d+\.\d+)/(?P<longitud>\d+\.\d+)/$', views.getLocalEspecificByLatLong, name='getLocalByLatLong'),
    path('getLocalByName/<str:nomLocal>/', views.getLocalEspecificByName, name='getLocalByName'),
    url(r'updateLocalByLatLong/(?P<nomLocal>[^/]+)/(?P<latitud>\d+\.\d+)/(?P<longitud>\d+\.\d+)/$', views.updateLocalByLatLong, name='updateLocalByLatLong'),
    path('updateLocalByName/<str:nomLocal>/', views.updateLocalByName, name='updateLocalByName'),
    path('createLocal/', views.postNewLocal, name='createLocal'),
    path('deleteLocalByLatLong/', views.deleteLocalByLatLong, name='deleteByLatLong'),
    path('deleteLocalByNom/', views.deleteLocalByName, name='deleteByName'),

    #############################################################
    #   VISTES DES DE LA WEB                                    #
    #############################################################

    path('registrar_nou_usuari/', views.paginaRegistrarse, name='Registrar'),
    path('map/', views.mostrarMapa, name='mapa'),
    url(r'info_especifica/(?P<nomLocal>[^/]+)/(?P<latitud>\d+\.\d+)/(?P<longitud>\d+\.\d+)/$', views.mostrarPuntEspecific, name='informacio'),
    path('inicia_sessio/', views.loginPage, name='inicia sessio'),
    path('tancar_sessio/', views.logout, name='Tancar sessio'),
    path('el_meu_espai/', views.profilePage, name='Espai'),
    path('actualitzar_camps/<str:codi>/', views.updateUsuari, name='Actualitzacio'),
    path('baixa_usuari/', views.baixa, name='baixa'),
    path('nouPunt/', views.crearNouPuntInteres, name='nou punt'),
    path('poblacions_per_provincia/', views.ciutatsPerProvincia, name='poblacionsxprovincies'),
    path('estadistiques/', views.res_ajax_estadistiques, name='ajaxestadistiques')
]