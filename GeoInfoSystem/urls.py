from django.urls import path

from GeoInfoSystem import views

urlpatterns = [
    path('allPuntsInteres/', views.getPuntsInteres, name='TotsPuntsInteres')
]