from django.core.exceptions import FieldDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth import logout as do_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from rest_framework import status, request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Exceptions import NoContingut
from GeoInfoSystem.models import *
from GeoInfoSystem.serializers import *
from GeoInfoSystem.forms import *
from Exceptions import *
from django.core import serializers
from ast import literal_eval
#from MySQLdb._exceptions import OperationalError
from django.db.utils import OperationalError
from PIL import Image
from django.conf import settings
from detect_delimiter import detect
from random import sample
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import re
import random
import urllib.parse
# Create your views here.
################################################################
################################################################
#                       VISTES WEB                             #
################################################################
################################################################

"""
Mètode auxiliar en la que es van passant les paraules que es volen i es cerquen a la base de dades
"""
def trobarParaula(paraula):
    return paraulesClauGIS.objects.all().filter(paraula=paraula)[0].paraula
""" 
Mètode que permet visualitzar la pàgina d'inici
"""
def home(request):
    titol_tfg=trobarParaula('Treball Fi de Grau')
    sistema=trobarParaula('Sistema')
    Informacio=trobarParaula('Informació')
    geografica=trobarParaula('Geogràfica')
    sistemaGIS=trobarParaula('sistema GIS')
    puntsminus=paraulesClauGIS.objects.all().filter(paraula='punts')[1].paraula
    puntsmajus=trobarParaula('Punts')
    interes=trobarParaula('interès')
    mapa=trobarParaula('mapa')
    punt=trobarParaula('punt')
    Mapa=paraulesClauGIS.objects.all().filter(paraula='mapa')[1].paraula
    pInteresMinus=puntsminus+' d\''+interes
    pInteresMajus=puntsmajus+' d\''+interes
    pInteresSingMinus=punt+' d\''+interes
    sIG=sistema+' d\''+Informacio+' '+geografica
    return render(request, "home/home.html",{'titol':titol_tfg, 'sig':sIG, 'sistemaGIS':sistemaGIS,
                                             'puntsInteres':pInteresMinus, 'PuntsInteres':pInteresMajus,
                                             'mapa':mapa, 'Mapa':Mapa, 'puntInteres':pInteresSingMinus})

"""
Mètode que mostra la pàgina per a registrar un nou usuari
"""
def paginaRegistrarse(request):
    if request.method == 'POST':
        password1=request.POST['password1']
        nou_usuari = User()
        nou_usuari.username=request.POST['username']
        if request.POST['first_name']:
            nou_usuari.first_name=request.POST['first_name']
        if request.POST['last_name']:
            nou_usuari.last_name = request.POST['last_name']
        nou_usuari.email=request.POST['email']
        nou_usuari.set_password(password1)
        print(nou_usuari)
        nou_usuari.save()
        return redirect("/")
    t_nom=trobarParaula("Nom")
    t_usuari=trobarParaula("Usuari")
    t_nomUsuari=t_nom+" d'"+t_usuari
    t_correuElectronic=trobarParaula("Correu Electrònic")
    t_cognom=trobarParaula("Cognom")
    t_contrassenya=trobarParaula("Contrasenya")

    return render(request, "usuaris/registrar1.html", {'label_nom':t_nom, 'label_nomUsuari':t_nomUsuari,
                                                       'label_correuElectronic':t_correuElectronic,
                                                       'label_cognom':t_cognom, 'label_contrasenya':t_contrassenya})

"""
Mètode AJAX que comprova les dades d'entrada del formulari del registre d'usuaris en la web.
Permet registrar-se quan l'usuari és nou, osigui no hi ha cap nom d'usuari igual en la base de dades, la contrassenya té més de 8 caràcters,
ambdues contrassenyes són iguals i el mail introduït té un format mail.
"""
def check_values_register_data(request):
    username = urllib.parse.unquote(request.GET['username'])
    password1 = urllib.parse.unquote(request.GET['password1'])
    password2 = urllib.parse.unquote(request.GET['password2'])
    email = urllib.parse.unquote(request.GET['email'])
    data = {}
    data['tot_ok']="true"
    if User.objects.all().filter(username=username):
        data['tot_ok']="false"
    if len(password1) < 8:
        data['tot_ok'] = "false"
    if password1 != password2:
        data['tot_ok']="false"
    if email:
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if not re.search(regex, email):
            data['tot_ok'] = "false"
    res_json = json.dumps(data)
    return HttpResponse(res_json, content_type='json')

"""
Mètode AJAX que permet comtrolar si les dades del formulari del registre estan plenes o buides.
En cas que les dades estiguin plenes, retorna fals i permet registrar-se, en altre cas, no.
"""
def check_empty_register_data(request):
    if request.method == 'GET':
        username=urllib.parse.unquote(request.GET['username'])
        first_name=urllib.parse.unquote(request.GET['first_name'])
        last_name=urllib.parse.unquote(request.GET['last_name'])
        password1=urllib.parse.unquote(request.GET['password1'])
        password2=urllib.parse.unquote(request.GET['password2'])
        email=urllib.parse.unquote(request.GET['email'])
        data={}
        if username == "" or first_name == "" or last_name == "" or password1 == "" or password2 == "" or email == "":
            data['buit'] = "true"
        else:
            data['buit'] = "false"
        res_json = json.dumps(data)
        return HttpResponse(res_json, content_type="json")

"""
Mètode que permet mostrar el mapa, punt central del sistema GIS. 
"""
def mostrarMapa(request):
    puntsInteresCercats = puntInteres.objects.all()
    localsimp = local.objects.all()

    claus_foranes_categories_local = local.objects.all().values_list('categoria', flat=True)
    categoriesCercades = categoriaLocal.objects.all().filter(pk__in = claus_foranes_categories_local)

    claus_foranes_localitzacio_puntInteres = puntInteres.objects.all().values_list('localitat', flat=True)
    localitzacionsC = localitzacio.objects.all().filter(pk__in=claus_foranes_localitzacio_puntInteres)

    locals = serializers.serialize("json", localsimp)
    punts = serializers.serialize("json", puntsInteresCercats)
    categoriesMapa = serializers.serialize("json", categoriesCercades)
    localitzacions = serializers.serialize("json", localitzacionsC)

    rand_id_puntInteres = random.choice(list(puntInteres.objects.all().values_list('id',flat=True)))

    pIntRand_latitud = str(puntInteres.objects.all().filter(id=rand_id_puntInteres)[0].latitud)
    pIntRand_longitud = str(puntInteres.objects.all().filter(id=rand_id_puntInteres)[0].longitud)
    nom_local_rand = local.objects.all().filter(localitzacio=rand_id_puntInteres)[0].nomLocal
    categoriesDB = categoriaLocal.objects.all()
    categoriesDB=serializers.serialize('json', categoriesDB)

    grafic=False
    num_locals = local.objects.all().count()
    categories = categoriaLocal.objects.all()
    data = {}
    for categoria in categories:
        data[categoria] = local.objects.all().filter(categoria=categoria).count()
    num_locals_actius = puntInteres.objects.all().filter(actiu=True).count()
    num_locals_no_actius = puntInteres.objects.all().filter(actiu=False).count()
    poblacions_catalunya=localitzacio.objects.all()
    grafic_b64_usos_categories = 'buit'
    grafic_actius_noactius = 'buit'
    if num_locals != 0 and num_locals_actius + num_locals_no_actius!= 0:
        grafic=True
        cat=data.keys()
        slices=data.values()
        colors=['#2AAD27','#2A81CB','#CB2B3E','#CB8427','#FFD326']
        plt.pie(slices, labels=cat, colors=colors,startangle=90, autopct = '%1.1f%%')
        plt.title('Usos de locals presents en el sistema GIS per categories.')
        plt.legend()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300)
        grafic_b64_usos_categories=base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
        buf.close()
        plt.close()
        cat=['Actius', 'No actius']
        slices=[num_locals_actius, num_locals_no_actius]
        colors=['#5D6D7E', '#EC7063']
        plt.pie(slices, labels=cat, colors=colors,startangle=90, autopct='%1.1f%%')
        plt.title('Percentatge de locals actius i no actius presents en el sistema GIS.')
        plt.legend(loc="center right")
        buf=io.BytesIO()
        plt.savefig(buf,format='png', dpi=300)
        grafic_actius_noactius=base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
        buf.close()
        plt.close()

    return render(request, "puntsGeografics/map.html", {'latitudRand': pIntRand_latitud, 'longitudRand': pIntRand_longitud, 'nomLocalRand':nom_local_rand,
                                                        'puntsInteres': punts, 'locals': locals, 'categoriesMapa': categoriesMapa,
                                                        'localitzacionsMapa':localitzacions, 'categoriesDB':categoriesDB,
                                                        'grafic_usos_categories':grafic_b64_usos_categories,
                                                        'grafic_actius_noactius':grafic_actius_noactius,
                                                        'hi_ha_grafic':grafic})

"""
Mètode que renderitza la pàgina que permet fer consultes al sistema GIS
"""
def estadistiques(request):
    provincies = localitzacio.objects.all().values_list('provincia', flat=True).distinct()
    dict = {}
    i = 1
    for res in provincies:
        dict['prov' + str(i)] = res
        i = i + 1
    provincies = json.dumps(dict)
    fk_pobles_puntsInteres = puntInteres.objects.all().values_list('localitat', flat=True)
    poblesTgn = localitzacio.objects.all().filter(provincia='Tarragona', id__in=fk_pobles_puntsInteres).values_list('ciutat', 'comarca')
    dict = {}
    i = 1
    for res in poblesTgn:
        dict['poble' + str(i)] = res[0] + " (" + res[1] + "), " + "Tarragona"
        i = i + 1
    print(dict['poble1'])
    poblesDeTgn = json.dumps(dict)
    tipus = categoriaLocal.objects.all()
    categoriesT = serializers.serialize('json', tipus)
    localitzacions = localitzacio.objects.all()
    localitzacions = serializers.serialize('json', localitzacions)
    return render(request, "puntsGeografics/estadistiques.html", {'totesLocalitzacions':localitzacions,'totesCategories': categoriesT, 'poblesTGN': poblesDeTgn, 'provincies':provincies, 'primeraLocalitatLlista':dict['poble1']})

"""
Mètode AJAX auxiliar al mètode anterior. Aquest permet que el mòdul estadístic no estigui buit a l'inici, sinó que tal com l'usuari
entra en la vista de la web, ja vegi les estadístiques inicials mostrades en la part inferior de la pantalla.
"""
def estadistiques_inicials(request):
    resultatsInicials = {}
    res = {}
    categoria = urllib.parse.unquote(request.GET['categoria'])
    ciutat=urllib.parse.unquote(request.GET['poblacio']).split(' (')[0]
    categoriaInicial = categoriaLocal.objects.all().filter(categoria=categoria)[0]
    pobleInicial = localitzacio.objects.all().filter(ciutat=ciutat)[0]
    actiu = False
    # RESULTAT AMB ELS FILTRES ESTABLERTS
    punt_filtre1 = puntInteres.objects.all().filter(localitat=pobleInicial, actiu=actiu)
    llocs_filtre1 = local.objects.all().filter(localitzacio__in=punt_filtre1, categoria=categoriaInicial)
    fk_id_puntInteres = local.objects.all().filter(localitzacio__in = punt_filtre1, categoria=categoriaInicial).values_list('localitzacio_id', flat=True)
    puntsInteresLatLng = puntInteres.objects.all().filter(id__in = fk_id_puntInteres)
    res_lat_lng = serializers.serialize('json', puntsInteresLatLng)
    res_filtre1 = serializers.serialize('json', llocs_filtre1)
    res['FiltresAplicats'] = res_filtre1
    res['numResultats'] = str(len(llocs_filtre1))
    res['puntinteresFiltresAplicats'] = res_lat_lng
    resultatsInicials['FitresEstablerts'] = res

    res = {}
    # RESULTAT ON SURTEN TOTS ELS PUNTS/LOCALS DEL MATEIX POBLE (TANT ACTIUS COM NO ACTIUS)
    punt_filtre1 = puntInteres.objects.all().filter(localitat=pobleInicial)
    llocs_filtre1 = local.objects.all().filter(localitzacio__in=punt_filtre1)
    fk_id_puntInteres = local.objects.all().filter(localitzacio__in=punt_filtre1).values_list('localitzacio_id', flat=True)
    puntsInteresLatLng = puntInteres.objects.all().filter(id__in=fk_id_puntInteres)
    res_lat_lng = serializers.serialize('json', puntsInteresLatLng)
    res_filtre1 = serializers.serialize('json', llocs_filtre1)
    res['puntsPoble'] = res_filtre1
    res['numMateixPoble'] = str(len(llocs_filtre1))
    res['puntsInterespuntsMateixPoble'] = res_lat_lng
    resultatsInicials['FiltreMateixPoble'] = res

    res = {}
    # RESULTAT NEGANT EL ACTIU MATEIXA CATEGORIA
    punt_filtre1 = puntInteres.objects.all().filter(localitat=pobleInicial, actiu=not actiu)
    llocs_filtre1 = local.objects.all().filter(localitzacio__in=punt_filtre1, categoria=categoriaInicial)
    fk_id_puntInteres = local.objects.all().filter(localitzacio__in=punt_filtre1, categoria=categoriaInicial).values_list('localitzacio_id',flat=True)
    puntsInteresLatLng = puntInteres.objects.all().filter(id__in=fk_id_puntInteres)
    res_lat_lng = serializers.serialize('json', puntsInteresLatLng)
    res_filtre1 = serializers.serialize('json', llocs_filtre1)
    res['resNegatActiuMateixaCat'] = res_filtre1
    res['numResNegatActiuMateixaCat'] = str(len(llocs_filtre1))
    res['resPuntInteresNegatActiuMateixaCat'] = res_lat_lng
    resultatsInicials['FiltreNegatActiuMateixaCat'] = res

    res = {}
    # RESULTAT MATEIX POBLE, ACTIU QUE VE I NO MATEIXA CATEGORIA
    punt_filtre1 = puntInteres.objects.all().filter(localitat=pobleInicial, actiu=actiu)
    altresCategories_filtre1 = categoriaLocal.objects.all().exclude(categoria=categoriaInicial)
    llocs_filtre1 = local.objects.all().filter(localitzacio__in=punt_filtre1, categoria__in=altresCategories_filtre1)
    fk_id_puntInteres = local.objects.all().filter(localitzacio__in=punt_filtre1, categoria__in=altresCategories_filtre1).values_list('localitzacio_id', flat=True)
    puntsInteresLatLng = puntInteres.objects.all().filter(id__in=fk_id_puntInteres)
    res_lat_lng = serializers.serialize('json', puntsInteresLatLng)
    res_filtre1 = serializers.serialize('json', llocs_filtre1)
    res['resMateixPobleNoMateixaCat'] = res_filtre1
    res['numresMateixPobleNoMateixaCat'] = str(len(llocs_filtre1))
    res['resPuntInteresMateixPobleNoMateixaCat'] = res_lat_lng
    resultatsInicials['FiltreMateixPobleNoMateixaCat'] = res

    res = {}
    # RESTULTAT NO MATEIX POBLE, ACTIU QUE VE I MATEIXA CATEGORIA
    punt_filtre1 = puntInteres.objects.all().exclude(localitat=pobleInicial).filter(actiu=actiu)
    llocs_filtre1 = local.objects.all().filter(localitzacio__in=punt_filtre1, categoria=categoriaInicial)
    fk_id_puntInteres = local.objects.all().filter(localitzacio__in=punt_filtre1,categoria=categoriaInicial).values_list('localitzacio_id', flat=True)
    puntsInteresLatLng = puntInteres.objects.all().filter(id__in=fk_id_puntInteres)
    res_lat_lng = serializers.serialize('json', puntsInteresLatLng)
    res_filtre1 = serializers.serialize('json', llocs_filtre1)
    res['resNoMateixPobleMateixaCat'] = res_filtre1
    res['numResNoMateixPobleMateixaCat'] = str(len(llocs_filtre1))
    res['resPuntInteresNoMateixPobleMateixaCat'] = res_lat_lng
    resultatsInicials['FiltreNoMateixPobleMateixaCat'] = res

    res = {}
    # RESULTAT NO MATEIX POBLE, ACTIU NEGAT I NO MATEIXA CATEGORIA
    punt_filtre1 = puntInteres.objects.all().exclude(localitat=pobleInicial).filter(actiu=not actiu)
    altresCategories_filtre1 = categoriaLocal.objects.all().exclude(categoria=categoriaInicial)
    llocs_filtre1 = local.objects.all().filter(localitzacio__in=punt_filtre1, categoria__in=altresCategories_filtre1)
    fk_id_puntInteres = local.objects.all().filter(localitzacio__in=punt_filtre1,categoria__in=altresCategories_filtre1).values_list('localitzacio_id', flat=True)
    puntsInteresLatLng = puntInteres.objects.all().filter(id__in=fk_id_puntInteres)
    res_lat_lng = serializers.serialize('json', puntsInteresLatLng)
    res_filtre1 = serializers.serialize('json', llocs_filtre1)
    res['resNoMateixPobleNoMateixaCategoria'] = res_filtre1
    res['numResNoMateixPobleNoMateixaCategoria'] = str(len(llocs_filtre1))
    res['resPuntInteresNoMateixPobleNoMateixaCategoria'] = res_lat_lng
    resultatsInicials['FiltreNoMateixPobleNoMateixaCat'] = res

    res = {}
    # RESULTAT AMB TOTES LES DADES DE LA DB
    punt_filtre1 = puntInteres.objects.all()
    llocs_filtre1 = local.objects.all().filter(localitzacio__in=punt_filtre1)
    fk_id_puntInteres = local.objects.all().filter(localitzacio__in=punt_filtre1).values_list('localitzacio_id', flat=True)
    puntsInteresLatLng = puntInteres.objects.all().filter(id__in=fk_id_puntInteres)
    res_lat_lng = serializers.serialize('json', puntsInteresLatLng)
    res_filtre1 = serializers.serialize('json', llocs_filtre1)
    res['infoDB'] = res_filtre1
    res['numinfoDB'] = str(len(llocs_filtre1))
    res['puntsIntresinfoDB'] = res_lat_lng
    resultatsInicials['FiltreTotaDB'] = res

    initial_statistics_data = json.dumps(resultatsInicials)
    return HttpResponse(initial_statistics_data, content_type='json')

"""
Mètode que permet executar la vista d'una pantalla informativa d'un punt específic.
Controla que les dades siguin correctes, en altre cas, informarà amb la vista de l'error i anira a la pàgina d'inici.
"""
def mostrarPuntEspecific(request, nomLocal,latitud, longitud):
    nomLocal = urllib.parse.unquote(nomLocal)
    try:
        punt = puntInteres.objects.all().filter(latitud=latitud, longitud=longitud)[0]
        if not punt:
            raise NoContingut
        loc = local.objects.all().filter(nomLocal=nomLocal, localitzacio=punt)
        if not loc:
            raise NoContingut
    except Exception or NoContingut:
        return redirect('/v1/geoInfoSystem/error/')
    puntInteresC = puntInteres.objects.all().filter(latitud=latitud, longitud=longitud)
    p = puntInteresC[0]
    localitat  = p.localitat
    print(localitat)
    localEspecific = local.objects.all().filter(nomLocal=nomLocal)
    categoria = localEspecific[0].categoria
    l=local.objects.all().filter(nomLocal=nomLocal)[0]
    imatge_local=imageLocal.objects.all().filter(local=l.id)
    if imatge_local:
        imatge_local=imatge_local[0].imatge.url
        # per a les imatges posades a la base de dades inicials
        if imatge_local.split("/")[2] == 'CasaMevaRedim.jpg' or imatge_local.split("/")[2] == 'firaReusRedim.jpg' or imatge_local.split("/")[2] == 'mcdonaldsVallsRedim.jpg' or imatge_local.split("/")[2] == 'urvCampusSesceladesRedim.jpg':
            imatge_local = "/media/photo/"+imatge_local.split("/")[2]
    else:
        imatge_local=''
    '''
    img_guardada_fs='base64'
    img_no_trobada='trobada'
    if imatge_local:
        imatge_local=imatge_local[0].imatge.decode('utf-8')
    else:
        img_local=imageLocal.objects.all().filter(local=l.id)
        if img_local:
            img_guardada_fs = 'sist_fitxers'
            imatge_local=img_local.imatge.url
        else:
            imatge_local=''
            img_no_trobada='no_trobada'
    '''
    print(categoria)
    altresPuntsInteres = list(puntInteres.objects.all().filter(localitat=p.localitat).exclude(latitud=latitud, longitud=longitud))
    """punts=[]
    for punt in altresPuntsInteres:
        punts+=[punt]
    locals = local.objects.all().exclude(nomLocal=nomLocal)
    altresLocals=[]
    for punt in punts:
        for l in locals:
            if l.localitzacio.localitat == punt.localitat:
                altresLocals+=[l]
    print(punts)
    print(altresLocals)"""
    punt = serializers.serialize("json", puntInteresC)
    localE = serializers.serialize("json", localEspecific)
    #altresLocals = serializers.serialize("json", altresLocals)
    #punts = serializers.serialize("json", punts)
    if len(altresPuntsInteres)>0:
        t_coordenades=trobarParaula('Coordenades')
        t_descripcio=trobarParaula('Descripció')
        t_localitzacio=trobarParaula('Localització')
        t_categoria=trobarParaula('Categoria')
        t_estatConservacio=trobarParaula('Estat de Conservació')
        t_anyConstruccio=trobarParaula('Any de Construcció')
        t_superficie=trobarParaula('Superfície')
        t_titol_pagina=trobarParaula("Informació Específica del Local")
        return render(request, "puntsGeografics/informacioDetallada.html", {'categoria':categoria,
                                                                            'localitat':localitat,'puntInteres':punt,
                                                                            'local': localE, 'altres': True,
                                                                            'imatge':imatge_local,'label_coordenades':t_coordenades,
                                                                            'label_descripcio':t_descripcio, 'label_localitzacio':t_localitzacio,
                                                                            'label_categoria':t_categoria, 'label_estatConservacio':t_estatConservacio,
                                                                            'label_anyConstruccio':t_anyConstruccio, 'label_superficie':t_superficie,
                                                                            'label_titol_pagina':t_titol_pagina})
    else:
        t_coordenades = trobarParaula('Coordenades')
        t_descripcio = trobarParaula('Descripció')
        t_localitzacio = trobarParaula('Localització')
        t_categoria = trobarParaula('Categoria')
        t_estatConservacio = trobarParaula('Estat de Conservació')
        t_anyConstruccio = trobarParaula('Any de Construcció')
        t_superficie = trobarParaula('Superfície')
        t_titol_pagina = trobarParaula("Informació Específica del Local")
        return render(request, "puntsGeografics/informacioDetallada.html", {'categoria':categoria,
                                                                            'localitat':localitat, 'puntInteres': punt,
                                                                            'local': localE, 'altres': False,
                                                                            'imatge':imatge_local,'label_coordenades':t_coordenades,
                                                                            'label_descripcio':t_descripcio, 'label_localitzacio':t_localitzacio,
                                                                            'label_categoria':t_categoria, 'label_estatConservacio':t_estatConservacio,
                                                                            'label_anyConstruccio':t_anyConstruccio, 'label_superficie':t_superficie,
                                                                            'label_titol_pagina':t_titol_pagina})

"""
Mètode AJAX auxiliar del mètode anterior que permet que quan en un punt d'una ciutat hi ha més punts, permet la obtenció dels altres punts específics i l'usuari hi pot accedir, sense cap problema.
"""
def ajax_altres_punts_mateixa_ciutat_info_especifica(request):
    if request.method == 'GET':
        nomLocal=urllib.parse.unquote(request.GET['nomLocal'])
        ciutat = urllib.parse.unquote(request.GET['ciutat'])
        latitud_punt_actual = float(request.GET['latitudPuntActual'])
        longitud_punt_actual = float(request.GET['longitudPuntActual'])
        data={}
        mateixa_ciutat = localitzacio.objects.all().filter(ciutat=ciutat.split('(')[0].replace(" (", ""))[0]
        altresPuntsInteres = puntInteres.objects.all().filter(localitat=mateixa_ciutat).exclude(latitud=latitud_punt_actual, longitud=longitud_punt_actual)
        punts = []
        for punt in altresPuntsInteres:
            punts += [punt]
        locals = local.objects.all().filter(localitzacio__in=altresPuntsInteres)
        categories=[]
        for loc in locals:
            categories+=[loc.categoria]
        categories_locals = categoriaLocal.objects.all().filter(categoria__in=categories)
        locals_localitat=serializers.serialize("json", locals)
        puntsInteres_localitat=serializers.serialize('json', punts)
        categories_locals = serializers.serialize('json', categories_locals)
        data['locals'] = locals_localitat
        data['puntsInteres'] = puntsInteres_localitat
        data['categories'] = categories_locals
        res_json = json.dumps(data)

        return HttpResponse(res_json, content_type='json')

"""
Mètode que permet executar la vista del log in i també permet processar les dades introduïdes.
En cas que el login sigui correcte, retornem a la pàgina d'inici.
"""
def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/")
        else:
            user = User.objects.all().filter(username=username)
            user=user[0]
            if user.check_password(password):
                if user.is_active:
                    login(request,user)
                    return redirect("/")
    titolPagina=trobarParaula('Inicia la sessió')
    t_contrassenya=trobarParaula('Contrasenya')
    t_nom=trobarParaula('Nom')
    t_usuari=trobarParaula('Usuari')
    t_nomUsuari=t_nom+" d'"+t_usuari
    return render(request, 'usuaris/login.html',{'titolPagina':titolPagina, 'label_contrassenya':t_contrassenya, 'label_nomusuari':t_nomUsuari})

"""
Mètode AJAX auxiliar del mètode anterior, el qual comprova si els inputs del login estan informats.
En cas que no estiguin informats, no et permetra fer login
"""
def checkInputsLogIn(request):
    if request.method == 'GET':
        data={}
        username = urllib.parse.unquote(request.GET['nomUsuari'])
        password = urllib.parse.unquote(request.GET['contrassenyaUsuari'])
        if username == "" or password == "":
            data['buit'] = "true"
        if username == "" and password == "":
            data['buit'] = "true"
        if username != "" and password != "":
            data['buit'] = "false"
        res_json = json.dumps(data)
        return HttpResponse(res_json, content_type="json")

"""
Mètode AJAX auxiliar del mètode del login que comprova si cert usuari, que ha posat les seves credencials estan bé o no.
En cas que estiguin bé, permetrà l'accès.
"""
def checkUserToLogIn(request):
    if request.method == 'GET':
        data={}
        username = urllib.parse.unquote(request.GET['nomUsuari'])
        passwd = urllib.parse.unquote(request.GET['contrassenyaUsuari'])
        userMaster = authenticate(username=username, password=passwd)
        if userMaster is not None:
            if userMaster.is_active:
                data['tot_ok'] = "true"
            else:
                data['tot_ok'] = "false"
        else:
            userMaster= User.objects.all().filter(username=username)
            if not userMaster:
                data['tot_ok'] = "false"
            else:
                user = userMaster[0]
                if user.check_password(passwd):
                    if user.is_active:
                        data['tot_ok'] = "true"
                    else:
                        data['tot_ok'] = "false"
                else:
                    data['tot_ok'] = "false"
        res_json = json.dumps(data)
        return HttpResponse(res_json, content_type='json')

"""
Mètode que permet fer el log out d'un usuari, que prèviament ha fet log in.
"""
def logout(request):
    do_logout(request)
    return redirect("/")

"""
Mètode que permet renderitzar la pàgina del perfil de l'usuari, sempre i quan aquest hagi fet log in prèviament.
A més, envia informació addicional sobre un punt random cada vegada que es recarrega la pàgina.
"""
@login_required(login_url='/v1/geoInfoSystem/inicia_sessio/')
def profilePage(request):
    # LOCAL RANDOM
    rand_id_puntInteres = random.choice(list(puntInteres.objects.all().values_list('id', flat=True)))
    pIntRand_latitud = str(puntInteres.objects.all().filter(id=rand_id_puntInteres)[0].latitud)
    pIntRand_longitud = str(puntInteres.objects.all().filter(id=rand_id_puntInteres)[0].longitud)
    nom_local_rand = local.objects.all().filter(localitzacio=rand_id_puntInteres)[0].nomLocal
    t_nom=trobarParaula("Nom")
    t_usuari=trobarParaula("Usuari")
    t_nomUsuari=t_nom+" d'"+t_usuari
    t_correuElectronic=trobarParaula("Correu Electrònic")
    t_cognom=trobarParaula("Cognom")
    t_contrasenya=trobarParaula("Contrasenya")
    t_sistemaGIS=trobarParaula("sistema GIS")
    t_mapa=trobarParaula("mapa")
    t_punts=paraulesClauGIS.objects.all().filter(paraula='punts')[1].paraula
    return render(request, "usuaris/profilePage.html", {'nomLocalRand':nom_local_rand,'latitudRand':pIntRand_latitud,
                                                        'longitudRand':pIntRand_longitud, 'label_nom':t_nom, 'label_cognom':t_cognom,
                                                        'label_nomUsuari':t_nomUsuari, 'label_correuElectronic':t_correuElectronic,
                                                        'label_contrasenya':t_contrasenya, 'label_sistemaGIS':t_sistemaGIS,
                                                        'label_punts':t_punts, 'label_mapa':t_mapa})

"""
Mètode que permet updatejar els camps de l'usuari sempre i quan s'hagi fet login.
Permet modificar el correu, el nom de la persona, el cognom i la contrassenya.
A més comprova que la URI estigui ben formada.
"""
@login_required(login_url='/v1/geoInfoSystem/inicia_sessio/')
def updateUsuari(request, codi):
    if request.method == 'POST':
        user_name=request.user
        if codi == 'actualitzaMail':
            mail1 = request.POST['email']
            User.objects.all().filter(username=user_name).update(email=mail1)
        elif codi == 'actualitzaNom':
            nom1 = request.POST['first_name']
            User.objects.all().filter(username=user_name).update(first_name=nom1)
        elif codi== 'actualitzaCognom':
            cognom1 = request.POST['last_name']
            User.objects.all().filter(username=user_name).update(last_name=cognom1)
        elif codi == 'actualitzaContrassenya':
            password1=request.POST['password']
            first_pass = User.objects.all().filter(username=user_name)[0].password.split('$')
            hasher = first_pass[0]
            salt = first_pass[1]  # grabbing salt from the first password of the database
            User.objects.all().filter(username=user_name).update(password=make_password(password1, salt, hasher))
        return redirect("/v1/geoInfoSystem/el_meu_espai/")
    else:
        codi = urllib.parse.unquote(codi)
        codiTallat = codi.split()
        if len(codiTallat)<4 or len(codiTallat)>=5:
            return redirect('/v1/geoInfoSystem/error/')
        if codiTallat[0].islower() and codiTallat[1].islower() and codiTallat[2].islower() and codiTallat[3].islower():
            return redirect('/v1/geoInfoSystem/error/')
        if codiTallat[0].lower() != 'e' or codiTallat[1].lower()!='n' or codiTallat[2].lower()!='c' or codiTallat[3].lower()!='p':
            return redirect('/v1/geoInfoSystem/error/')
        chMail = False
        if codiTallat[0].isupper():
            chMail = True
        chNom = False
        if codiTallat[1].isupper():
            chNom=True
        chCog = False
        if codiTallat[2].isupper():
            chCog = True
        chPass = False
        if codiTallat[3].isupper():
            chPass = True
        t_correuElectronic=trobarParaula('Correu Electrònic')
        t_nom=trobarParaula('Nom')
        t_cognom=trobarParaula("Cognom")
        t_contrasenya=trobarParaula("Contrasenya")
        return render(request, "usuaris/updateUsuari.html",{'chMail':chMail,
                                                            'chNom':chNom, 'chCog':chCog, 'chPass':chPass,
                                                            'label_correuElectronic':t_correuElectronic,
                                                            'label_nom':t_nom, 'label_cognom':t_cognom,
                                                            'label_contrasenya':t_contrasenya})

"""
Mètode AJAX auxiliar que verifica que els camps del mail estiguin informats per a poder actualizar-lo.
"""
def comprovar_mails_update_usuari_empty(request):
    if request.method == 'GET':
        mail1=request.GET['mail1']
        mail2=request.GET['mail2']
        data={}
        data['tot_ok']='true'
        if mail1 == "" or mail2 == "":
            data['tot_ok']='false'
        res_json=json.dumps(data)
        return HttpResponse(res_json,content_type='json')

"""
Mètode AJAX que comprova que els mails siguin iguals i dóna l'OK per a actualitzar-lo.
"""
def comprovar_mails_update_usuari(request):
    if request.method == 'GET':
        mail1 = request.GET['mail1']
        mail2 = request.GET['mail2']
        data={}
        data['tot_ok']='true'
        if mail1 != mail2:
            data['tot_ok']='false'
        else:
            regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
            if not re.search(regex, mail1) or not re.search(regex, mail2):
                data['tot_ok']='false'
        res_json = json.dumps(data)
        return HttpResponse(res_json, content_type='json')

"""
Mètode AJAX auxiliar que verifica que els camps del nom estiguin informats per a poder actualizar-lo.
"""
def comprovar_noms_update_usuari_empty(request):
    if request.method == 'GET':
        nom1=request.GET['nom1']
        nom2=request.GET['nom2']
        data = {}
        data['tot_ok'] = 'true'
        if nom1 == "" or nom2 == "":
            data['tot_ok'] = 'false'
        res_json = json.dumps(data)
        return HttpResponse(res_json, content_type='json')

"""
Mètode AJAX que comprova que els noms siguin iguals i que el nom que es posa sigui diferent al nom d'usuari, en aquest cas,
dóna l'OK per a actualitzar-lo. 
"""
def comprovar_noms_update_usuari(request):
    if request.method=='GET':
        nom1=request.GET['nom1']
        nom2=request.GET['nom2']
        nomUsuari = request.GET['nomUsuari']
        data={}
        data['tot_ok'] = 'true'
        if nom1 != nom2:
            data['tot_ok']='false'
        else:
            if nom1 == nomUsuari:
                data['tot_ok']='false'
        res_json = json.dumps(data)
        return HttpResponse(res_json, content_type='json')

"""
Mètode AJAX auxiliar que verifica que els camps del cognom estiguin informats per a poder actualizar-lo.
"""
def comprovar_cognom_update_usuari_empty(request):
    if request.method == 'GET':
        cognom1=request.GET['cognom1']
        cognom2=request.GET['cognom2']
        data = {}
        data['tot_ok'] = 'true'
        if cognom1 == "" or cognom2 == "":
            data['tot_ok'] = 'false'
        res_json = json.dumps(data)
        return HttpResponse(res_json, content_type='json')

"""
Mètode AJAX que comprova que els cognoms siguin iguals i dóna l'OK per a actualitzar-lo.
"""
def comprovar_cognom_update_usuari(request):
    if request.method == 'GET':
        cognom1=request.GET['cognom1']
        cognom2=request.GET['cognom2']
        data={}
        data['tot_ok'] = 'true'
        if cognom1 != cognom2:
            data['tot_ok']='false'
        res_json = json.dumps(data)
        return HttpResponse(res_json, content_type='json')

"""
Mètode AJAX auxiliar que verifica que els camps de la contrassenya estiguin informats per a poder actualizar-lo.
"""
def comprovar_contrassenya_update_usuari_empty(request):
    if request.method == 'GET':
        passwd1=request.GET['passwd1']
        passwd2=request.GET['passwd2']
        data = {}
        data['tot_ok'] = 'true'
        if passwd1 == "" or passwd2 == "":
            data['tot_ok'] = 'false'
        res_json = json.dumps(data)
        return HttpResponse(res_json, content_type='json')

"""
Mètode AJAX que comprova que les contrassenyes tinguin més de 8 caràcters alfanumèrics i que siguin iguals. En aquest cas, dóna l'OK per a actualitzar-lo.
"""
def comprovar_contrassenya_update_usuari(request):
    if request.method == 'GET':
        passwd1=request.GET['passwd1']
        passwd2=request.GET['passwd2']
        data={}
        data['tot_ok'] = 'true'
        if passwd1 != passwd2:
            data['tot_ok']='false'
        else:
            if len(passwd1) < 8:
                data['tot_ok']='false'
        res_json=json.dumps(data)
        return HttpResponse(res_json, content_type='json')

"""
Mètode que permet donar de baixa un usuari.
"""
def baixa(request):
    curr_usr = request.user
    User.objects.all().filter(username=curr_usr).delete()
    return redirect("/")

"""
Mètode que renderitza la pàgina de no autoritzat.
"""
def unauthorizedpage(response):
    return render(response, "errors/NoAutoritzat.html", {})

"""
Mètode que renderitza la pàgina d'error
"""
def errorpage(request):
    return render(request, "errors/ErrorFile.html", {})

"""
Mètode AJAX auxiliar per a totes aquelles pantalles que requereixin les ciutats de la BD i les recupera.
"""
def ciutatsPerProvincia(request):
    if request.method == 'GET':
        provincia = request.GET['provincia']
        localitzacions = localitzacio.objects.all().filter(provincia=provincia).values_list('ciutat', 'comarca')
        dict={}
        res={}
        i=1
        for elem in localitzacions:
            dict['localitzacio'+str(i)] = elem[0]+" ("+elem[1]+")"
            i = i +1
        res['data'] = dict
        loc = json.dumps(res)
        return HttpResponse(loc, content_type='json')

"""
Mètode AJAX que retorna les ciutats d'una província en específic
"""
def ciutatsPerProvincia_estadistiques(request):
    if request.method == 'GET':
        provincia = request.GET['provincia']
        fk_localitzacio = puntInteres.objects.all().values_list('localitat', flat=True)
        localitzacions=localitzacio.objects.all().filter(provincia=provincia, id__in=fk_localitzacio).values_list('ciutat', 'comarca')
        dict={}
        res={}
        i=1
        for elem in localitzacions:
            dict['localitzacio'+str(i)]=elem[0]+" ("+elem[1]+")"
            i=i+1
        res['data'] = dict
        loc = json.dumps(res)
        return HttpResponse(loc, content_type='json')

"""
Mètode AJAX que permet fer les estadístiques al instant que l'usuari va modificant els filtres.
"""
def res_ajax_estadistiques(request):
    if request.method == 'GET':
        ciutat = urllib.parse.unquote(request.GET['poblacio'])
        actiu = urllib.parse.unquote(request.GET['actiu'])
        categoria = urllib.parse.unquote(request.GET['categoria'])
        bActiu = False
        cAux = ciutat.split(' (')[0]
        if actiu =='True':
            bActiu = True

        poble = localitzacio.objects.all().filter(ciutat = cAux)[0] #nom del poble
        categoriaC = categoriaLocal.objects.all().filter(categoria=categoria)[0] #categoria
        res = {}
        dict = {}
        # RESULTAT AMB ELS FILTRES ESTABLERTS
        punt = puntInteres.objects.all().filter(localitat = poble, actiu = bActiu)
        lloc = local.objects.all().filter(localitzacio__in = punt, categoria = categoriaC)
        fk_id_puntsInteres = local.objects.all().filter(localitzacio__in = punt, categoria = categoriaC).values_list('localitzacio_id', flat=True)
        res_lat_lng = puntInteres.objects.all().filter(id__in = fk_id_puntsInteres)
        res_json_lat_lng = serializers.serialize('json', res_lat_lng)
        data = serializers.serialize('json', lloc)
        dict['resFiltres'] = data
        dict['numlocalsTotsFiltres'] = str(len(lloc))
        dict['puntIntersFiltresActuals'] = res_json_lat_lng
        dict['descripcio'] = 'Resultat obtingut desprès d\'aplicar tots els filtres.'
        res['AllFilters'] = dict


        dict = {}
        # RESULTAT ON SURTEN TOTS ELS PUNTS/LOCALS DEL MATEIX POBLE (TANT ACTIUS COM NO ACTIUS)
        punt = puntInteres.objects.all().filter(localitat=poble)
        lloc = local.objects.all().filter(localitzacio__in=punt)
        fk_id_puntsInteres = local.objects.all().filter(localitzacio__in=punt).values_list('localitzacio_id', flat=True)
        res_lat_lng = puntInteres.objects.all().filter(id__in=fk_id_puntsInteres)
        res_json_lat_lng = serializers.serialize('json', res_lat_lng)
        data = serializers.serialize('json', lloc)
        dict['llocMateixPoble'] = data
        dict['numLocalsMateixPoble'] = str(len(lloc))
        dict['puntsIntersMateixPoble'] = res_json_lat_lng
        dict['descripcio'] = 'Tots els locals que es troben en la mateixa ciutat (tant actius com no actius).'
        res['FilterMateixPoble'] = dict

        dict = {}
        # RESULTAT NEGANT EL ACTIU MATEIXA CATEGORIA
        punt = puntInteres.objects.all().filter(localitat=poble, actiu=not bActiu)
        lloc = local.objects.all().filter(localitzacio__in=punt, categoria=categoriaC)
        fk_id_puntsInteres = local.objects.all().filter(localitzacio__in=punt, categoria=categoriaC).values_list('localitzacio_id', flat=True)
        res_lat_lng = puntInteres.objects.all().filter(id__in=fk_id_puntsInteres)
        res_json_lat_lng = serializers.serialize('json', res_lat_lng)
        data = serializers.serialize('json', lloc)
        dict['llocFilterNegat'] = data
        dict['numLocalsNegantActiuMateixaCategoria'] = str(len(lloc))
        dict['puntInteresNegatActiuMateixaCategoria'] = res_json_lat_lng
        dict['descripcio'] = 'Resultats obtinguts deprès d\'haver negat si és actiu i mantenint la mateixa categoria.'
        res['FilterNegantActiu'] = dict


        dict = {}
        # RESULTAT MATEIX POBLE, ACTIU QUE VE I NO MATEIXA CATEGORIA
        punt = puntInteres.objects.all().filter(localitat=poble, actiu=bActiu)
        altresCategories = categoriaLocal.objects.all().exclude(categoria=categoria)
        lloc = local.objects.all().filter(localitzacio__in=punt, categoria__in=altresCategories)
        fk_id_puntsInteres = local.objects.all().filter(localitzacio__in=punt, categoria__in=altresCategories).values_list('localitzacio_id', flat=True)
        res_lat_lng = puntInteres.objects.all().filter(id__in=fk_id_puntsInteres)
        res_json_lat_lng = serializers.serialize('json', res_lat_lng)
        data = serializers.serialize('json', lloc)
        dict['filtreEstrany'] = data
        dict['numResMateixPobleNotMateixaCategoria'] = str(len(lloc))
        dict['puntsInteresfiltreExtrany'] = res_json_lat_lng
        dict['descripcio'] = 'Resultat obtingut de aplicar el mateix poble amb l\'actiu que s\'ha donat i una categoria diferent a la donada.'
        res['FiltreResMateixPobleNotCategoriaDonada'] = dict

        dict = {}
        # RESTULTAT NO MATEIX POBLE, ACTIU QUE VE I MATEIXA CATEGORIA
        punt = puntInteres.objects.all().exclude(localitat=poble).filter(actiu=bActiu)
        lloc = local.objects.all().filter(localitzacio__in=punt, categoria=categoriaC)
        fk_id_puntsInteres = local.objects.all().filter(localitzacio__in=punt, categoria=categoriaC).values_list('localitzacio_id', flat=True)
        res_lat_lng = puntInteres.objects.all().filter(id__in=fk_id_puntsInteres)
        res_json_lat_lng = serializers.serialize('json', res_lat_lng)
        data = serializers.serialize('json', lloc)
        dict['filtreEstrany']=data
        dict['numResNoMateixPobleMateixaCategoria'] = str(len(lloc))
        dict['puntsInteresfiltreExtrany'] = res_json_lat_lng
        dict['descripcio'] = 'Resultat de aplicar altres pobles i actiu que s\'ha donat i la mateixa categoria donada.'
        res['FiltreResNoMateixPobleMateixaCategoria'] = dict

        dict = {}
        # RESULTAT NO MATEIX POBLE, ACTIU NEGAT I NO MATEIXA CATEGORIA
        punt = puntInteres.objects.all().exclude(localitat=poble).filter(actiu=not bActiu)
        llCategories = categoriaLocal.objects.all().exclude(categoria=categoriaC)
        lloc = local.objects.all().filter(localitzacio__in=punt, categoria__in=llCategories)
        fk_id_puntsInteres = local.objects.all().filter(localitzacio__in=punt, categoria__in=llCategories).values_list('localitzacio_id', flat=True)
        res_lat_lng = puntInteres.objects.all().filter(id__in=fk_id_puntsInteres)
        res_json_lat_lng = serializers.serialize('json', res_lat_lng)
        data = serializers.serialize('json', lloc)
        dict['filtreEstrany'] = data
        dict['numResNoMateixPobleNoMateixaCategoria'] = str(len(lloc))
        dict['PuntInteresfiltreExtrany'] = res_json_lat_lng
        dict['descripcio'] = 'Resultat de aplicar un poble diferent al donat, actiu negat i no mateixa categoria.'
        res['FiltreResNoMateixPobleNoMateixaCategoria'] = dict

        dict = {}
        # RESULTAT AMB TOTES LES DADES DE LA DB
        punt = puntInteres.objects.all()
        lloc = local.objects.all().filter(localitzacio__in=punt)
        fk_id_puntsInteres = local.objects.all().filter(localitzacio__in=punt).values_list('localitzacio_id', flat=True)
        res_lat_lng = puntInteres.objects.all().filter(id__in=fk_id_puntsInteres)
        res_json_lat_lng = serializers.serialize('json', res_lat_lng)
        data = serializers.serialize('json', lloc)
        dict['llocsDB'] = data
        dict['numElemsReals'] = str(len(lloc))
        dict['puntsInteresLlocsDB'] = res_json_lat_lng
        dict['descripcio'] = 'Totes les dades.'
        res['RealsDB'] = dict
        res_json = json.dumps(res)
        return HttpResponse(res_json, content_type='json')

"""
Mètode que permet accedir a la url d'afegir un nou punt sempre i quan aquest usuari sigui adimistrador de la pàgina.
"""
@user_passes_test(lambda u: u.is_superuser)
def crearNouPuntInteres(request):       #Només pots entrar si és administrador de la pàgina
    provincies = localitzacio.objects.all().values_list('provincia', flat=True).distinct()
    i=1
    provinciesMostrarAux={}
    for prov in provincies:
        provinciesMostrarAux['prov'+str(i)] = prov
        i = i + 1
    provinciesMostrar=json.dumps(provinciesMostrarAux)
    categories = categoriaLocal.objects.all()
    categoriesMostrar = serializers.serialize("json", categories)
    poblacions = localitzacio.objects.all().filter(provincia='Tarragona')
    poblacionsMostrar = serializers.serialize("json", poblacions)
    if request.method == 'POST':
        # em ve nomPunt,lat<espai>lng
        altresPuntsPerProcessar = json.loads(request.POST['altresPunts'])
        puntNou = request.POST['puntPerProcessar1']
        nomLocal = request.POST['nomLocal']
        descripcioLocal = request.POST['descripcioLocal']
        tipus = request.POST['tipus']
        llocActiu = request.POST['llocActiu']
        superficie = request.POST['superficie'].replace(',', '.')
        localitat = request.POST['poblacio'] #em ve: poblacio<espai>(comarca),<espai>provincia
        puntuacio = request.POST['p']
        any = request.POST['any']
        midaLlistaString = request.POST['midaLlista']

        superficie=float(superficie)
        puntSplit = puntNou.split(",") #tinc el nom del punt, q no el vull per a res[0] <-> lat lng [1]
        coordenades = puntSplit[1].split(" ") #lat[0] long[1] en format string
        latitud=float(coordenades[0])
        longitud=float(coordenades[1])
        actiu=False
        sLocalitat = localitat.split(' (')  #em ve: poblacio<espai>(comarca),<espai>provincia
        poblacio = sLocalitat[0]
        poblacio = localitzacio.objects.all().filter(ciutat=poblacio)[0]
        if llocActiu == "True":
            actiu=True
        nouPunt = puntInteres(latitud=latitud, longitud=longitud, actiu=actiu, superficie=superficie, localitat=poblacio)
        nouPunt.save()
        p = puntInteres.objects.all().filter(latitud=latitud, longitud=longitud)[0]
        categoria = categoriaLocal.objects.all().filter(categoria=tipus)[0]
        localNou = local(localitzacio=p, nomLocal=nomLocal, estat_conservacio=int(puntuacio), categoria=categoria, anyConstruccio=int(any), descripcio=descripcioLocal)
        localNou.save()
        localGuardat = local.objects.all().filter(localitzacio=p, nomLocal=nomLocal, estat_conservacio=int(puntuacio),
                                                  categoria=categoria, anyConstruccio=int(any),
                                                  descripcio=descripcioLocal)[0]
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            l = local.objects.all().filter(id=localGuardat.id)
            img_local = imageLocal()
            img_local.local = l[0]
            img_local.imatge = form.cleaned_data['image']
            img_local.save()
            imatge_local_emmagatzemat = imageLocal.objects.all().filter(local=localGuardat.id)[0]
            path_img_saved = urllib.parse.unquote(imatge_local_emmagatzemat.imatge.url)  # /media/photo/<nom_foto>
            media_root = settings.MEDIA_ROOT.split('/')[0].replace('\\', '/')
            path = media_root + path_img_saved
            path = path.replace('/', '\\')
            img_pil = Image.open(path)
            resize = (800, 600)
            img_width, img_height = float(img_pil.size[0]), float(img_pil.size[1])
            if img_width <= resize[0] and img_height <= resize[1]:
                img_pil.save(path, format="PNG")  # guardem la imatge en png
            else:
                width = resize[0]
                height = resize[1]
                if img_width > img_height or img_width == img_height:
                    width = resize[0]
                    height = int(img_height * (resize[0] / img_width))
                else:
                    height = resize[1]
                    width = int(img_width * (resize[1] / img_height))
                img_pil = img_pil.resize((width, height), Image.ANTIALIAS)
                img_pil.save(path, format="PNG")  # guardem la imatge en png
        '''
        quan la imatge té molta qualitat, el processament triga molt i llavors peta la comunicacio amb la db
        imatge_pujada = request.FILES['image'].file.read()  # bytes de la imatge
        img_pil = Image.open(io.BytesIO(imatge_pujada))  # obrir imatge amb pil
        in_mem_file = io.BytesIO()               # Preparem zona de memòria virtual
        # algorisme de redimensionar imatge. En cas que la foto sigui més petita, la deix igual per mantenir
        # la proporció de la foto
        resize = (800, 600)
        img_width, img_height = float(img_pil.size[0]), float(img_pil.size[1])
        if img_width <= resize[0] and img_height <= resize[1]:
            img_pil.save(in_mem_file, format="PNG")  # guardem la imatge en png
        else:
            width = resize[0]
            height = resize[1]
            if img_width > img_height or img_width == img_height:
                width = resize[0]
                height = int(img_height * (resize[0] / img_width))
            else:
                height = resize[1]
                width = int(img_width * (resize[1] / img_height))
            img_pil = img_pil.resize((width, height), Image.ANTIALIAS)
            img_pil.save(in_mem_file, format="PNG")  # guardem la imatge en png

        in_mem_file.seek(0) # reset file pointer to start
        img_bytes = in_mem_file.read()  # tinc els bytes despres de redimensionar
        b64_imatge_bytes = base64.encodebytes(img_bytes)  #codifico b64

        t_bd_imatges=imatges_locals()       #guardo a la bd
        t_bd_imatges.imatge=b64_imatge_bytes
        t_bd_imatges.local=localGuardat
        t_bd_imatges.save()
        '''
        dict = {}
        llista = []
        i = 0
        for punt in altresPuntsPerProcessar:
            puntSplit = punt.split(",")
            dict["punt"] = puntSplit[0] + "," + puntSplit[1]
            i = i + 1
            llista += [dict]
            dict = {}
        midaLlista = int(midaLlistaString)
        punts = json.dumps(llista)
        if len(altresPuntsPerProcessar) == 1:
            if altresPuntsPerProcessar[0].split(',')[0] == '--- Siusplau selecciona un punt ---':
                return redirect("/v1/geoInfoSystem/map/")
        else:
            midaLlista = int(midaLlistaString)
            punts = json.dumps(llista)
            t_sistemaGIS=trobarParaula("sistema GIS")
            t_mapa = trobarParaula('mapa')
            t_mapa_majus = paraulesClauGIS.objects.all().filter(paraula='mapa')[1].paraula
            t_punt_majus=paraulesClauGIS.objects.all().filter(paraula='punt')[1].paraula
            t_nomLocal=trobarParaula('Nom del local')
            t_categoria=trobarParaula('Categoria')
            t_superficie=trobarParaula('Superfície')
            t_provincia=trobarParaula('Província')
            t_localitat=trobarParaula('Localitat')
            t_estatConservacio=trobarParaula('Estat de Conservació')
            t_anyConstruccio=trobarParaula('Any de Construcció')
            t_fotoLocal=trobarParaula('Insereix foto del local')
            t_actiu=trobarParaula('Actiu')
            return render(request, "puntsGeoGrafics/afegirNouPunt.html", {'provincies':provinciesMostrar ,
                                                                          'categories': categoriesMostrar,
                                                                          'poblacions':poblacionsMostrar,
                                                                          'punts': punts,'lenLlista':midaLlista,
                                                                          'label_sistemaGIS':t_sistemaGIS,
                                                                          'label_mapa':t_mapa, 'label_mapa_majus':t_mapa_majus,
                                                                          'label_punt_majus':t_punt_majus, 'label_nomLocal':t_nomLocal,
                                                                          'label_categoria':t_categoria, 'label_superficie':t_superficie,
                                                                          'label_provincia':t_provincia, 'label_localitat':t_localitat,
                                                                          'label_estatConservacio':t_estatConservacio, 'label_anyConstruccio':t_anyConstruccio,
                                                                          'label_foto':t_fotoLocal, 'label_actiu': t_actiu})
    t_sistemaGIS=trobarParaula("sistema GIS")
    t_mapa=trobarParaula('mapa')
    t_mapa_majus=paraulesClauGIS.objects.all().filter(paraula='mapa')[1].paraula
    t_punt_majus = paraulesClauGIS.objects.all().filter(paraula='punt')[1].paraula
    t_nomLocal = trobarParaula('Nom del local')
    t_categoria = trobarParaula('Categoria')
    t_superficie = trobarParaula('Superfície')
    t_provincia = trobarParaula('Província')
    t_localitat = trobarParaula('Localitat')
    t_estatConservacio = trobarParaula('Estat de Conservació')
    t_anyConstruccio = trobarParaula('Any de Construcció')
    t_fotoLocal = trobarParaula('Insereix foto del local')
    t_actiu = trobarParaula('Actiu')
    return render(request, "puntsGeografics/afegirNouPunt.html", {'provincies':provinciesMostrar,
                                                                  'categories':categoriesMostrar,
                                                                  'poblacions':poblacionsMostrar,
                                                                  'punts':[], 'lenLlista':0,
                                                                  'label_sistemaGIS':t_sistemaGIS,
                                                                  'label_mapa':t_mapa, 'label_mapa_majus':t_mapa_majus,
                                                                  'label_punts_majus':t_punt_majus, 'label_nomLocal':t_nomLocal,
                                                                  'label_categoria':t_categoria, 'label_superficie':t_superficie,
                                                                  'label_provincia':t_provincia, 'label_localitat':t_localitat,
                                                                  'label_estatConservacio':t_estatConservacio, 'label_anyConstruccio':t_anyConstruccio,
                                                                  'label_foto':t_fotoLocal, 'label_actiu': t_actiu})

"""
Mètode AJAX auxiliar del anterior mètode, que permet comprovar que els camps estiguin informats
"""
def check_values_new_point_empty(request):
    if request.method == 'GET':
        nomLocal = urllib.parse.unquote(request.GET['nomLocal'])
        descripcioLocal = urllib.parse.unquote(request.GET['descripcioLocal'])
        superficie = request.GET['superficie']
        any = request.GET['any']
        foto=urllib.parse.unquote(request.GET['foto'])
        data={}
        data['tot_ok']='true'
        if nomLocal == '' or descripcioLocal == '' or superficie == '' or any == '' or foto == '':
            data['tot_ok']='false'
        res_json = json.dumps(data)
        return HttpResponse(res_json, content_type='json')

"""
Mètode AJAX auxiliar que comprova que els camps del formulari del local, per al nou punt estiguin ben informats.
"""
def check_values_new_point(request):
    if request.method == 'GET':
        nomLocal = urllib.parse.unquote(request.GET['nomLocal'])
        superficie = request.GET['superficie'].replace(',', '.')
        categoria = request.GET['tipus']
        any = request.GET['any']
        poble = urllib.parse.unquote(request.GET['poblacio']).split(" (")[0]
        ciutat = localitzacio.objects.all().filter(ciutat=poble)[0]
        data = {}
        data['tot_ok'] = 'true'
        if local.objects.all().filter(nomLocal=nomLocal).count() == 0:
            data['tot_ok']='true'
        else:
            pInteres_nou_localitat = local.objects.all().filter(nomLocal = nomLocal)[0].localitzacio.localitat
            local_nou_categoria = local.objects.all().filter(nomLocal=nomLocal)[0].categoria.categoria
            if ciutat == pInteres_nou_localitat and categoria == local_nou_categoria: #permeto que en la mateixa ciutat hi hagi dos punts d'interes amb el mateix nom però diferent categoria
                data['tot_ok']='false'
        if data['tot_ok'] == 'true':
            try:
                sup=float(superficie)
            except Exception or ValueError:
                data['tot_ok']='false'
            try:
                year=int(any)
                if year <0:
                    data['tot_ok']='false'
            except Exception or ValueError:
                data['tot_ok']='false'
        res_json = json.dumps(data)
        return HttpResponse(res_json, content_type='json')

"""
Mètode AJAX que permet que els botons d'ordenació del mòdul estadísitc ordenin en dos sentits diferents:
    * De la A - Z o de Z - A, en cas que siguin paraules.
    * De 0 - N o de N - 0, en cas que siguin nombres.
"""
def ordenament(request):
    if request.method=='GET':
        tipusOrdenament=request.GET['tipusOrdenacio']
        informacio = urllib.parse.unquote(request.GET['informacio'])
        json_data=json.loads(informacio)
        localsEnviats=[]
        for elem in json_data:
            dict = literal_eval(elem)
            localsEnviats.append(dict)
        if tipusOrdenament == 'nomLocal':
            reverse=True
            if request.GET['sentit'] == 'descendent':
                reverse=False
            nomsLocals=[]
            for dict in localsEnviats:
                nomsLocals.append(dict['nomLocal'])
            nomsLocals_ordenat=sorted(nomsLocals, reverse=reverse)
            new_dict={}
            ordenat = []
            for nom_local_ordenat in nomsLocals_ordenat:
                dict=trobarLocal(nom_local_ordenat, localsEnviats)
                new_dict['nomLocal']=dict['nomLocal']
                new_dict['url']=dict['url']
                new_dict['categoria']=dict['colsText1']
                new_dict['estatConservacio']=dict['estatConservacio']
                new_dict['anyConstruccio']=dict['colsText2']
                new_dict['localitat']=dict['colsText3']
                new_dict['descripcio']=dict['colsText4']
                ordenat.append(new_dict)
                new_dict={}
            res_json=json.dumps(ordenat)
            return HttpResponse(res_json, content_type='json')
        if tipusOrdenament == 'categoria':
            reverse = True
            if request.GET['sentit'] == 'descendent':
                reverse = False
            categoriesEnviades=[]
            aux={}
            for dict in localsEnviats:
                aux['nomLocal']=dict['nomLocal']
                aux['url']=dict['url']
                aux['categoria']=dict['colsText1']
                aux['estatConservacio']=dict['estatConservacio']
                aux['anyConstruccio']=dict['colsText2']
                aux['localitat']=dict['colsText3']
                aux['descripcio']=dict['colsText4']
                categoriesEnviades.append(aux)
                aux={}

            categories_ordenades=sorted(categoriesEnviades, key=lambda k: k['categoria'], reverse=reverse)
            res_json=json.dumps(categories_ordenades)
            return HttpResponse(res_json, content_type='json')
        if tipusOrdenament == 'estatConservacio':
            reverse=False
            if request.GET['sentit'] == 'descendent':
                reverse=True
            estatsConservacioEnviats=[]
            aux={}
            for dict in localsEnviats:
                aux['nomLocal'] = dict['nomLocal']
                aux['url'] = dict['url']
                aux['categoria'] = dict['colsText1']
                aux['estatConservacio'] = dict['estatConservacio']
                aux['anyConstruccio'] = dict['colsText2']
                aux['localitat'] = dict['colsText3']
                aux['descripcio'] = dict['colsText4']
                estatsConservacioEnviats.append(aux)
                aux = {}
            estats_conservacio_ordenats=sorted(estatsConservacioEnviats, key=lambda k: k['estatConservacio'], reverse=reverse)
            res_json=json.dumps(estats_conservacio_ordenats)
            return HttpResponse(res_json, content_type='json')
        if tipusOrdenament == 'anyConstruccio':
            reverse=False
            if request.GET['sentit']=='descendent':
                reverse=True
            anysConstruccioEnviats=[]
            aux={}
            for dict in localsEnviats:
                aux['nomLocal'] = dict['nomLocal']
                aux['url'] = dict['url']
                aux['categoria'] = dict['colsText1']
                aux['estatConservacio'] = dict['estatConservacio']
                aux['anyConstruccio'] = int(dict['colsText2'])
                aux['localitat'] = dict['colsText3']
                aux['descripcio'] = dict['colsText4']
                anysConstruccioEnviats.append(aux)
                aux = {}
            anys_construccio_ordenats=sorted(anysConstruccioEnviats, key=lambda k: k['anyConstruccio'], reverse=reverse)
            res_json=json.dumps(anys_construccio_ordenats)
            return HttpResponse(res_json, content_type='json')
        if tipusOrdenament == 'localitat':
            reverse = True
            if request.GET['sentit'] == 'descendent':
                reverse = False
            localitatsEnviades=[]
            aux={}
            for dict in localsEnviats:
                aux['nomLocal'] = dict['nomLocal']
                aux['url'] = dict['url']
                aux['categoria'] = dict['colsText1']
                aux['estatConservacio'] = dict['estatConservacio']
                aux['anyConstruccio'] = dict['colsText2']
                aux['localitat'] = dict['colsText3']
                aux['descripcio'] = dict['colsText4']
                localitatsEnviades.append(aux)
                aux = {}
            localitats_ordenades=sorted(localitatsEnviades, key=lambda k: k['localitat'], reverse=reverse)
            res_json=json.dumps(localitats_ordenades)
            return HttpResponse(res_json, content_type='json')

"""
Mètode auxiliar del anterior que permet cercar el local que es busca.
"""
def trobarLocal(nomLocal, llistatDiccionaris):
    for dict in llistatDiccionaris:
        if dict['nomLocal'] == nomLocal:
            return dict

"""
Mètode que permet el sistema d'importació de dades i que verifica que tot el que hi ha dins del fitxer CSV
està bé i no hi ha cap error. En aquest cas, entrariem a la següent fase i podrem anar pujant els locals un a un.
"""
@user_passes_test(lambda u: u.is_superuser)
def importacio_dades_per_csv(request):
    errors = []
    if request.method == 'POST':
        fitxer=request.FILES['fitxer'].file.read()
        str_file_value=fitxer.decode('latin1')
        file = str_file_value.splitlines()
        delimiter=detect(file[0])       #recupero el delimitador del string
        camps={0:'Nom del local', 1:'Latitud', 2:'Longitud', 3:'Descripció', 4:'Tipus', 5:'Superficie', 6:'Província',
               7:'Localitat', 8: 'Estat de conservació', 9:'Any de construcció', 10:'Actiu'}
        data={}
        list_of_dicts=[]
        cmpt_lines = 0
        if not file[1:]:
            errors.append('El fitxer està buit.')
            list_of_errors = []
            dict_of_error = {}
            ind = 0
            for error in errors:
                dict_of_error['error' + str(ind)] = error
                ind = ind + 1
                list_of_errors.append(dict_of_error)
                dict_of_error = {}
            errors = json.dumps(list_of_errors)
            return render(request, "motorImportacio/motorImportacio.html", {'errorsImportacio': errors})
        for line in file[1:]:
            cmpt_lines = cmpt_lines + 1
            if '' in line.split(delimiter):
                errors.append("La línia {} al camp {}, no està ple. Es requereix que estiguin tots els camps plens.".format(cmpt_lines + 1, camps[line.split(delimiter).index('')]))
            else:
                i = 0
                list_data_new_local=line.split(delimiter)
                nom_local=list_data_new_local[0]
                try:
                    latitud=float(list_data_new_local[1].replace(',', '.'))
                except:
                    errors.append(
                        "La línia {} al camp {}, no té un format numèric vàlid o no és un valor. Revisi el camp.".format(
                            cmpt_lines + 1, camps[line.split(delimiter).index(list_data_new_local[1])]))
                    continue
                try:
                    longitud=float(list_data_new_local[2].replace(',', '.'))
                except:
                    errors.append(
                        "La línia {} al camp {}, no té un format numèric vàlid o no és un valor. Revisi el camp.".format(
                            cmpt_lines + 1, camps[line.split(delimiter).index(list_data_new_local[2])]))
                    continue
                descripcio=list_data_new_local[3].replace("\"", "'")
                try:
                    tipus=list_data_new_local[4].title()
                    categoria_local=categoriaLocal.objects.all().filter(categoria=tipus)
                    if not categoria_local:
                        raise Exception
                except:
                    cat_bones=[]
                    categories_valides = categoriaLocal.objects.all()
                    for elem in categories_valides:
                        cat_bones.append(elem.categoria)
                    errors.append(
                        "La línia {} al camp {}, no té una categoria vàlida. Revisi el camp. Les vàlides són: {}".format(
                            cmpt_lines + 1, camps[line.split(delimiter).index(list_data_new_local[2])], cat_bones))
                    continue
                try:
                    superficie=float(list_data_new_local[5].replace(',', '.'))
                except:
                    errors.append(
                        "La línia {} al camp {}, no té un format numèric vàlid o no és un valor. Revisi el camp.".format(
                            cmpt_lines + 1, camps[line.split(delimiter).index(list_data_new_local[5])]))
                    continue
                try:
                    provincia=list_data_new_local[6].title()
                    localitat=list_data_new_local[7]
                    print(localitat)
                    ciutat=localitzacio.objects.all().filter(provincia=provincia, ciutat=localitat)
                    print(ciutat)
                    if not ciutat:
                        raise Exception
                except:
                    ciutat_semblant=localitzacio.objects.all().filter(provincia=provincia, ciutat__icontains=localitat)
                    if ciutat_semblant:
                        s_ciutats_semblants=' '
                        text="La línia {} al camp {}, no existeix.".format(cmpt_lines + 1, camps[line.split(delimiter).index(list_data_new_local[8])])
                        for ciutat in ciutat_semblant:
                            s_ciutats_semblants+=ciutat.ciutat+' '
                        text+="Potser volies dir:{}".format(s_ciutats_semblants)
                        errors.append(text)
                    else:
                        errors.append(
                            "La línia {} al camp {}, no existeix. Revisi el camp.".format(
                                cmpt_lines + 1, camps[line.split(delimiter).index(list_data_new_local[8])]))
                    continue
                try:
                    estat_conservacio=int(list_data_new_local[8])
                    if estat_conservacio<0 or estat_conservacio>5:
                        raise Exception
                except:
                    errors.append(
                        "La línia {} al camp {}, no és un valor o no està entre 0 i 5. Revisi el camp.".format(
                            cmpt_lines + 1, camps[line.split(delimiter).index(list_data_new_local[8])]))
                    continue
                try:
                    any_construccio=int(list_data_new_local[9])
                    if any_construccio < 0:
                        raise Exception
                except:
                    errors.append(
                        "La línia {} al camp {}, no és un valor o és negatiu. Revisi el camp.".format(
                            cmpt_lines + 1, camps[line.split(delimiter).index(list_data_new_local[9])]))
                    continue
                try:
                    actiu=list_data_new_local[10]
                    if actiu != "Sí" and actiu != "No":
                        raise Exception
                except:
                    errors.append(
                        "La línia {} al camp {}, ha de ser 'Sí' o 'No'. Revisi el camp.".format(
                            cmpt_lines + 1, camps[line.split(delimiter).index(list_data_new_local[10])]))
                    continue
                try:
                    localitat_poblacio = localitzacio.objects.all().filter(provincia=provincia, ciutat=localitat)[0]
                    actiuBool=False
                    if actiu == 'Sí':
                        actiuBool=True
                    punts_interes_iguals=puntInteres.objects.all().filter(latitud=latitud, longitud=longitud, actiu=actiuBool,superficie=superficie,localitat=localitat_poblacio)
                    if punts_interes_iguals:
                        cat_local_csv=categoriaLocal.objects.all().filter(categoria=tipus)[0]
                        locals_iguals=local.objects.all().filter(localitzacio=punts_interes_iguals, nomLocal=nom_local, estat_conservacio=estat_conservacio, anyConstruccio=any_construccio,descripcio=descripcio, categoria=cat_local_csv)
                        if locals_iguals:
                            raise Exception
                except:
                    errors.append("La línia {}, ja forma part del sistema GIS.".format(cmpt_lines+1))
                    continue
                for elem in line.split(delimiter):
                    if i == 4 or i == 6 or i == 7:
                        data['camp'+str(i)]=elem.title()
                    else:
                        data['camp' + str(i)] = elem
                    i = i + 1
                data['descartat']='false'
            list_of_dicts.append(data)
            data={}
        if errors:
            list_of_errors=[]
            dict_of_error={}
            ind=0
            for error in errors:
                dict_of_error['error'+str(ind)]=error
                ind=ind+1
                list_of_errors.append(dict_of_error)
                dict_of_error={}
            errors=json.dumps(list_of_errors)
            t_nomLocal=trobarParaula('Nom del Local')
            t_latitud=trobarParaula('Latitud')
            t_longitud=trobarParaula('Longitud')
            t_descripcio=trobarParaula('Descripció')
            t_categoria=trobarParaula('Categoria')
            t_provincia=trobarParaula('Província')
            t_localitzacio=trobarParaula('Localització')
            t_estatConservacio=trobarParaula('Estat de Conservació')
            t_anyConservacio=trobarParaula('Any de Construcció')
            t_actiu=trobarParaula('Actiu')
            t_superficie=trobarParaula("Superfície")
            return render(request, "motorImportacio/motorImportacio.html", {'errorsImportacio': errors, 'label_nomLocal':t_nomLocal,'label_latitud':t_latitud,
                                                                            'label_longitud':t_longitud, 'label_descripcio':t_descripcio, 'label_categoria':t_categoria,
                                                                            'label_provincia':t_provincia, 'label_localitzacio':t_localitzacio, 'label_estatConservacio':t_estatConservacio,
                                                                            'label_anyConstruccio':t_anyConservacio, 'label_actiu': t_actiu, 'label_superficie':t_superficie})
        else:
            res_json = json.dumps(list_of_dicts)
            return render(request, "motorImportacio/dadesImportades.html", {'infoJSON':res_json})
    t_nomLocal = trobarParaula('Nom del Local')
    t_latitud = trobarParaula('Latitud')
    t_longitud = trobarParaula('Longitud')
    t_descripcio = trobarParaula('Descripció')
    t_categoria = trobarParaula('Categoria')
    t_provincia = trobarParaula('Província')
    t_localitzacio = trobarParaula('Localització')
    t_estatConservacio = trobarParaula('Estat de Conservació')
    t_anyConservacio = trobarParaula('Any de Construcció')
    t_actiu = trobarParaula('Actiu')
    t_superficie = trobarParaula("Superfície")
    return render(request, "motorImportacio/motorImportacio.html", {'errorsImportacio': errors, 'label_nomLocal':t_nomLocal,'label_latitud':t_latitud,
                                                                    'label_longitud':t_longitud, 'label_descripcio':t_descripcio, 'label_categoria':t_categoria,
                                                                    'label_provincia':t_provincia, 'label_localitzacio':t_localitzacio, 'label_estatConservacio':t_estatConservacio,
                                                                    'label_anyConstruccio':t_anyConservacio, 'label_actiu': t_actiu, 'label_superficie':t_superficie})

"""
Mètode del formulari del motor d'importació que permet emmagatzemar la informació provinent del fitxer CSV.
En cas que hi hagin encara nous locals, et retorna a la pàgina anterior per a poder seguir pujant els altres.
"""
def guardar_local_per_importacioCSV(request):
    if request.method == 'POST':
        id_local_importat=request.POST['id-local-csv']
        num_elems=int(request.POST['num-elems-'+id_local_importat])
        foto = request.FILES['image' + id_local_importat]
        nomLocal=request.POST['input-nomLlocal-'+id_local_importat]
        latitud=request.POST['input-latitud-'+id_local_importat]
        longitud=request.POST['input-longitud-'+id_local_importat]
        descripcio=request.POST['input-descripcio-'+id_local_importat]
        categoria_local=request.POST['input-tipus-'+id_local_importat]
        provincia=request.POST['input-provincia-'+id_local_importat]
        poble=request.POST['input-localitat-'+id_local_importat]
        estat_conservacio=request.POST['input-estatConservacio-'+id_local_importat]
        any_construccio=request.POST['input-anyConstruccio-'+id_local_importat]
        actiu=request.POST['input-actiu-'+id_local_importat]
        superficie=request.POST['input-superficie-'+id_local_importat]
        # guardar el nou local al sistema GIS
        localitat=localitzacio.objects.all().filter(provincia=provincia, ciutat=poble)[0]
        actiuBool=False
        if actiu=="Sí":
            actiuBool=True
        pInteres_new=puntInteres(latitud=float(latitud), longitud=float(longitud), actiu=actiuBool, superficie=float(superficie), localitat=localitat)
        pInteres_new.save()
        pInteres_c=puntInteres.objects.all().filter(latitud=float(latitud), longitud=float(longitud), actiu=actiuBool, superficie=float(superficie), localitat=localitat)[0]
        cat_nouLocal=categoriaLocal.objects.all().filter(categoria=categoria_local)[0]
        local_new=local(localitzacio=pInteres_c, nomLocal=nomLocal, estat_conservacio=int(estat_conservacio), categoria=cat_nouLocal, anyConstruccio=int(any_construccio), descripcio=descripcio)
        local_new.save()
        # guardar la foto
        localGuardat=local.objects.all().filter(localitzacio=pInteres_c, nomLocal=nomLocal, estat_conservacio=int(estat_conservacio), categoria=cat_nouLocal, anyConstruccio=int(any_construccio), descripcio=descripcio)[0]
        l = local.objects.all().filter(id=localGuardat.id)
        img_local = imageLocal()
        img_local.local = l[0]
        img_local.imatge = foto
        img_local.save()
        imatge_local_emmagatzemat = imageLocal.objects.all().filter(local=localGuardat.id)[0]
        path_img_saved = urllib.parse.unquote(imatge_local_emmagatzemat.imatge.url)  # /media/photo/<nom_foto>
        media_root = settings.MEDIA_ROOT.split('/')[0].replace('\\', '/')
        path = media_root + path_img_saved
        path = path.replace('/', '\\')
        img_pil = Image.open(path)
        resize = (800, 600)
        img_width, img_height = float(img_pil.size[0]), float(img_pil.size[1])
        if img_width <= resize[0] and img_height <= resize[1]:
            img_pil.save(path, format="PNG")  # guardem la imatge en png
        else:
            width = resize[0]
            height = resize[1]
            if img_width > img_height or img_width == img_height:
                width = resize[0]
                height = int(img_height * (resize[0] / img_width))
            else:
                height = resize[1]
                width = int(img_width * (resize[1] / img_height))
            img_pil = img_pil.resize((width, height), Image.ANTIALIAS)
            img_pil.save(path, format="PNG")  # guardem la imatge en png
        # tractar els altres locals que queden jeje
        altresLocalsPerPujar=request.POST['input-altresLocalsImportats-'+id_local_importat]
        print(altresLocalsPerPujar)
        if altresLocalsPerPujar != '' and num_elems>=1:
            list_dicts=[]
            data={}
            altresLocalsPerPujar=altresLocalsPerPujar.split('||')
            for newlocal in altresLocalsPerPujar:
                if newlocal:
                    info_nou_local=newlocal.split('<>')
                    nom_local_nou=info_nou_local[0]
                    latitud_nou_local=info_nou_local[1]
                    longitud_nou_local=info_nou_local[2]
                    superficie_nou_local=info_nou_local[3]
                    descripcio_nou_local=info_nou_local[4]
                    categoria_nou_local=info_nou_local[5]
                    provincia_nou_local=info_nou_local[6]
                    localitat_nou_local=info_nou_local[7]
                    estat_conservacio_nou_local=info_nou_local[8]
                    any_construccio_nou_local=info_nou_local[9]
                    actiu_nou_local=info_nou_local[10]
                    descartat=info_nou_local[11]
                    data['camp0']=nom_local_nou
                    data['camp1']=latitud_nou_local
                    data['camp2']=longitud_nou_local
                    data['camp3']=descripcio_nou_local
                    data['camp4']=categoria_nou_local
                    data['camp5']=superficie_nou_local
                    data['camp6']=provincia_nou_local
                    data['camp7']=localitat_nou_local
                    data['camp8']=estat_conservacio_nou_local
                    data['camp9']=any_construccio_nou_local
                    data['camp10']=actiu_nou_local
                    data['camp11']=descartat
                    list_dicts.append(data)
                    data={}
            res_json=json.dumps(list_dicts)
            return render(request, "motorImportacio/dadesImportades.html", {'infoJSON':res_json})
        else:
            return redirect('/v1/geoInfoSystem/map/')

"""
Mètode AJAX que el criden cadascun dels botons que hi ha per confirmar en el motor d'importació
i verifica que l'usuari hagi pujat la imatge.
"""
def comprovar_si_te_imatge_local_importacioCSV(request):
    if request.method == 'GET':
        imatge=urllib.parse.unquote(request.GET['imatge'])
        data={}
        data['tot_ok']='false'
        if imatge:
            data['tot_ok']='true'
        res_json=json.dumps(data)
        return HttpResponse(res_json, content_type='json')

"""
Mètode AJAX que comprova que hi ha un document CSV pujat i preparat per a ser importat.
"""
def comprovar_dades_entrada_importacio(request):
    if request.method=='GET':
        fitxer=urllib.parse.unquote(request.GET['fitxer'])
        data={}
        data['tot_ok']='true'
        if fitxer == '':
            data['tot_ok'] = 'false'
        res_json=json.dumps(data)
        return HttpResponse(res_json, content_type='json')
"""
AIXO ES PERQ AIXI ES COMPROVA SI ÉS SUPERUSUARI, EN ALTRE CAS NO ENTRARA
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def score_reset(self,...):
    ...
"""