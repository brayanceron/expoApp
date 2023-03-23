from django.contrib import admin
from .views import *
from django.urls import path,include
from django.contrib.auth.views import logout_then_login,LoginView
from django.conf.urls import handler404




urlpatterns = [
    path('home/', getCatalogoTutorias),
    path('getTutoria/',getTutoria),
    #path('currentuser/',currentuser),   #Borrar
    

    
    path('getCatalogoTutorias/', getCatalogoTutorias,name='getCatalogoTutorias'),
    path('getMisTutorias/', getMisTutorias,name='getMisTutorias'),
    path('getContenidoTutoria/<id_tutoria>', getContenidoTutoria,name='getContenidoTutoria'),   #ooooooooooo
    path('publicarTutoria/<id_profesor>', publicarTutoria,name='publicarTutoria'),             
    path('registrarEntrada/<id_tutoria>', registrarEntrada,name='registrarEntrada'),             #000000000
    path('getSolicitudes/', getSolicitudes,name='getSolicitudes'),
    path('getEntrada/<id_entrada>', getEntrada,name='getEntrada'),
    
    path('login/',LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',logout_then_login,name='logout'),
    path('signin/',signin,name='signin'),
    path('perfil/<correo>', perfil,name='perfil'),
    path('getTutoriaPublicada/<id_tutoria>', getTutoriaPublicada,name='getTutoriaPublicada'),
    
    
]

handler404=handler404

