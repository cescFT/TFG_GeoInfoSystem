from django.conf.urls import url
from django.urls import path

from GeoInfoSystem import views

urlpatterns = [
    path('allPuntsInteres/', views.getPuntsInteres, name='TotsPuntsInteres'),
    path('puntInteresByCity/', views.getPuntInteresByCity, name='pInteresCiutat'),
    path('puntInteresByCoordenades/', views.getPuntInteresEspecific, name='pInteresCoordenades'),
    url(r'updatePuntInteres/(?P<latitud>\d+\.\d+)/(?P<longitud>\d+\.\d+)/$', views.updatePuntInteres, name='pInteresUpdate'),
    path('newPuntInteres/', views.postNewPuntInteres, name='pInteresCreate'),
    path('provaDel/<str:puntInteres>', views.deletePuntInteres, name='provaQueryParamEliminar')
]