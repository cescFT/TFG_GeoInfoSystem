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
    path('altres_punts_mateixa_ciutat_info_especifica/', views.ajax_altres_punts_mateixa_ciutat_info_especifica, name='altrespunts'),
    path('inicia_sessio/', views.loginPage, name='inicia sessio'),
    path('tancar_sessio/', views.logout, name='Tancar sessio'),
    path('el_meu_espai/', views.profilePage, name='Espai'),
    path('actualitzar_camps/<str:codi>/', views.updateUsuari, name='Actualitzacio'),
    path('comprovar_mails_update/', views.comprovar_mails_update_usuari, name='mailsCheck'),
    path('comprovar_mails_buits_update/', views.comprovar_mails_update_usuari_empty, name='mailsCheckEmpty'),
    path('comprovar_noms_update/', views.comprovar_noms_update_usuari, name='nomsCheck'),
    path('comprovar_noms_buits_update/', views.comprovar_noms_update_usuari_empty, name='nomsCheckEmpty'),
    path('comprovar_cognoms_update/', views.comprovar_cognom_update_usuari, name='cognomsCheck'),
    path('comprovar_cognoms_buits_update/', views.comprovar_cognom_update_usuari_empty, name='cognomsCheckEmpty'),
    path('comprovar_contrassenya_update/', views.comprovar_contrassenya_update_usuari, name='passwdCheck'),
    path('comprovar_contrassenya_buits_update/', views.comprovar_contrassenya_update_usuari_empty, name='passwdCheckEmpty'),
    path('baixa_usuari/', views.baixa, name='baixa'),
    path('nouPunt/', views.crearNouPuntInteres, name='nou punt'),
    path('poblacions_per_provincia/', views.ciutatsPerProvincia, name='poblacionsxprovincies'),
    path('poblacions_per_provincia_estadistiques/', views.ciutatsPerProvincia_estadistiques, name='poblacionsEstadistiques'),
    path('estadistiquesGIS/', views.estadistiques, name='statistics'),
    path('estadistiques/', views.res_ajax_estadistiques, name='ajaxestadistiques'),
    path('estadistiques_inicials/', views.estadistiques_inicials, name='ajaxestadistiquesInicials'),
    path('comprovarInputsLogIn/', views.checkInputsLogIn, name="checkInputLogIn"),
    path('comprovarLogIn/', views.checkUserToLogIn, name="checklogin"),
    path('comprovarValorsBuitsRegistre/', views.check_empty_register_data, name="checkEmptyValuesRegister"),
    path('comprovarRegistre/', views.check_values_register_data, name="checkRegister"),
    path('comprovarValorsBuitsNouPunt/', views.check_values_new_point_empty, name='checkEmptyNewPoint'),
    path('comprovarDadesNouPunt/', views.check_values_new_point, name='checkDataNewPoint'),
    path('error/', views.errorpage, name='errorpage'),
    path('ordenacio/', views.ordenament, name='ordenamentSortida')
]