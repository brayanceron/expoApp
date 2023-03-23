"""BackEndAppfinal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import *
from appFinal.settings import *
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

#Esto es para subir archivos----------------------------------


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', root),
    
    #path('web/', include('FrontEndAppfinal.urls')),
    
    path('rutaUno/', rutaUno),
    path('getMisTutoriasEnProgresoEstudiante/', getMisTutoriasEnProgresoEstudiante),
    path('getMisTutoriasEnProgresoProfesor/', getMisTutoriasEnProgresoProfesor),
    path('getMisTutoriasPublicadas/', getMisTutoriasPublicadas),
    path('cambiarFotoPerfilUsuario/', cambiarFotoPerfilUsuario),
    path('cambiarFotoPerfilTutoria/', cambiarFotoPerfilTutoria),
    path('registrarUsuario/', registrarUsuario),
    
    
    path('getTutoria/', getTutoria),
    path('getTutoriaPublicada/', getTutoriaPublicada),
    path('getCatalogoTutorias/', getCatalogoTutorias),
    path('publicarTutoria/', publicarTutoria),
    path('getContenidoTutoria/', getContenidoTutoria),
    path('getEntrada/', getEntrada),
    path('registrarEntrada/', registrarEntrada),
    path('updateEntrada/', updateEntrada),
    
    path('getSolicitudesProfesor/', getSolicitudesProfesor),
    path('getSolicitudesEstudiante/', getSolicitudesEstudiante),
    
    path('rechazarSolicitud/', rechazarSolicitud),
    path('cancelarSolicitud/', cancelarSolicitud),
    path('borrarSolicitud/', borrarSolicitud),
    path('registrarSolicitud/', registrarSolicitud),
    path('aceptarSolicitud/', aceptarSolicitud),
        
    path('unirmeTutoria/', unirmeTutoria),
    
    
    path('getInfoUsuario/', getInfoUsuario),
    path('updateInfoUsuario/', updateInfoUsuario),
    path('updateTutoriaPublicada/', updateTutoriaPublicada),
    
    path('subirArchivotest/', subirArchivotest),
    path('subirArchivos/', subirArchivos),
    
    
    path('validarPermisoAccesoTutoria/', validarPermisoAccesoTutoria),
    path('validarPermisoAccesoEntrada/', validarPermisoAccesoEntrada),
    
    
    path('finalizarTutoria/', finalizarTutoria),
    
    path('descargar/',descargar),
    
    path('loginGoogle/',loginGoogle)
    
    #path(r'^media/(?P<path>.*)$', serve,{'document_root': MEDIA_ROOT}),
    #path(r'^static/(?P<path>.*)$', serve,{'document_root': STATIC_ROOT}),
    
]

#Esto es para subir archivos----------------------------------
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
               