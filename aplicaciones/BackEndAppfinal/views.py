import mimetypes
import os
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.core.files.storage import FileSystemStorage
from .consultasMogoDB import *
import json
from datetime import datetime
import uuid

from appFinal.settings import MEDIA_ROOT


def root(request):
    return HttpResponse("Oki")

@csrf_exempt 
def rutaUno(request):
    
    if request.method == 'GET':
        print("Peticion get recivida")
        return JsonResponse({"prueba_get":"OK","atributo2":"valor 2"})
    
    elif request.method == 'POST':
        print("Peticion post recivida")
        data =json.loads(request.body.decode("utf-8")) 
        print(data)
        print(data["datos_peticion"])
        return JsonResponse({"prueba_post":"OK"})
    
@csrf_exempt 
def getInfoUsuario(request):
    if request.method == 'POST':
        print("Buscando informacion de un usuario")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        correo=datarecivida['correo']
        
        listaR=json.loads(getInfoUsuarioMongo(correo))
        #print(listaR)
        return JsonResponse((listaR),safe=False)
    
@csrf_exempt 
def registrarUsuario(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
        correo=datarecivida['correo']
        rol=datarecivida['rol']
        nombre=datarecivida['nombre']
        
        
        if (validarCorreoExisteMongo(correo)==True): 
            return JsonResponse({},safe=False,status="428")
        
        st=str(crearUsuarioMongo(correo,rol,nombre))
        print("*** BACK ESTADO ***"+st)
 
        return JsonResponse({},safe=False,status=st)


@csrf_exempt #Este metodo solo es para la app movil
def loginGoogle(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
        correo=datarecivida['correo']
        rol=datarecivida['rol']
        nombre=datarecivida['nombre']
        url_google=datarecivida['url_google']
        
        
        if (validarCorreoExisteMongo(correo)==True): 
            return JsonResponse({},safe=False,status="428")
        else:
            st=str(crearUsuarioGoogleMongo(correo,rol,nombre,url_google))
            print("*** BACK ESTADO ***"+st)
            return JsonResponse({},safe=False,status=st)


@csrf_exempt 
def updateInfoUsuario(request):
    if request.method == 'POST':
        
        print("Actualizando informacion de un usuario")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        correo=datarecivida['correo']
        telefono=datarecivida['telefono']
        direccion=datarecivida['direccion']
        nombre=datarecivida['nombre']
        descripcion=datarecivida['descripcion']
        
        data={
            'correo':correo,
            'telefono':telefono,
            'direccion':direccion,
            'nombre':nombre,
            "descripcion":descripcion
        }
     
        #listaR=json.loads(updateInfoUsuarioMongo(data))
        #return JsonResponse((listaR),safe=False)
    
        state=updateInfoUsuarioMongo(data)
        return JsonResponse({},safe=False)


@csrf_exempt 
def updateTutoriaPublicada(request):
    if request.method == 'POST':
        
        print("Actualizando informacion de la tutoria")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        correo=datarecivida['correo']
        nombre=datarecivida['nombre']
        descripcion=datarecivida['descripcion']
        id_tutoria=datarecivida['id_tutoria']
        
        data={
            'correo':correo,
            'nombre':nombre,
            "descripcion":descripcion,
            "id_tutoria":id_tutoria
        }
     
        #listaR=json.loads(updateInfoUsuarioMongo(data))
        #return JsonResponse((listaR),safe=False)
    
        state=updateTutoriaPublicadaMongo(data)
        return JsonResponse({},safe=False)

@csrf_exempt 
def cambiarFotoPerfilUsuario(request):
    correo = request.POST["correo"] 
    infoFoto=subirFotoTutoria(request)  
    

    
    state=cambiarFotoPerfilUsuarioMongo(correo,infoFoto)
    return JsonResponse({},safe=False)


@csrf_exempt 
def cambiarFotoPerfilTutoria(request):
    id_tutoria = request.POST["id_tutoria"] 
    infoFoto=subirFotoTutoria(request)  
    

    
    state=cambiarFotoPerfilTutoriaMongo(id_tutoria,infoFoto)
    return JsonResponse({},safe=False)

@csrf_exempt 
def getMisTutoriasEnProgresoEstudiante(request):
    datarecivida =json.loads(request.body.decode("utf-8")) 
    
    correo=datarecivida['correo']
    id_usuario=getIdUsuarioMongo(correo)
    
    print("Enviando  tutorias del usuario: "+id_usuario )
    listaR=json.loads(getMisTutoriasEnProgresoEstudianteMongo(id_usuario)) #se convierte a json la cadena que viene en formato json
    return JsonResponse((listaR),safe=False)

@csrf_exempt 
def getMisTutoriasEnProgresoProfesor(request):
    datarecivida =json.loads(request.body.decode("utf-8")) 
    
    correo=datarecivida['correo']
    id_usuario=getIdUsuarioMongo(correo)
    
    print("Enviando  tutorias del usuario: "+id_usuario )
    listaR=json.loads(getMisTutoriasEnProgresoProfesorMongo(id_usuario)) #se convierte a json la cadena que viene en formato json
    return JsonResponse((listaR),safe=False)




@csrf_exempt 
def getMisTutoriasPublicadas(request):
    datarecivida =json.loads(request.body.decode("utf-8")) 
    
    correo=datarecivida['correo']
    id_usuario=getIdUsuarioMongo(correo)
    
    print("Enviando  tutorias del usuario: "+id_usuario )
    listaR=json.loads(getMisTutoriasPublicadasMongo(id_usuario)) #se convierte a json la cadena que viene en formato json
    return JsonResponse((listaR),safe=False)

    
@csrf_exempt 
def getTutoria(request):
    if request.method == 'POST':
        print("Buscando tutoria")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        
        id_tutoria=datarecivida['id_tutoria']
        #print("***** BACK *****"+str(id_tutoria))
        listaR=json.loads(getTutoriaMongo(id_tutoria))
        return JsonResponse((listaR),safe=False)

@csrf_exempt 
def getTutoriaPublicada(request):
    if request.method == 'POST':
        print("Buscando tutoria")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        
        id_tutoria=datarecivida['id_tutoria']
        #print("***** BACK *****"+str(id_tutoria))
        listaR=json.loads(getTutoriaPublicadaMongo(id_tutoria))
        return JsonResponse((listaR),safe=False)

@csrf_exempt 
def getCatalogoTutorias(request):
    if request.method == 'GET':
        print("Buscando todas tutoria")
        
        #hay que agregar un try aqui para validar que la peticion hay sido exitosa
        listaR=json.loads(getCatalogoTutoriasMongo())
        return JsonResponse((listaR),safe=False)
    
@csrf_exempt 
def getContenidoTutoria(request):
    if request.method == 'POST':
        print("Buscando Contenido de la tutoria")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        
        id_tutoria=datarecivida['id_tutoria']
        current_user_id=datarecivida['current_user_id']
        
        
        #print("****BACK*****"+current_user_id)
        listaR=json.loads(getContenidoTutoriaMongo(id_tutoria,current_user_id))
        if (str(listaR)=="500"):
            #print("---bk--- 500")
            return JsonResponse({},safe=False,status="500")
        elif (str(listaR)=="403"):
            #print("---bk--- 403")
            return JsonResponse({},safe=False,status="403")
        else:
            #print("---bk--- 200")
            return JsonResponse((listaR),safe=False,status="200")
        
        #return JsonResponse({"ok":"ok"},safe=False)



    
@csrf_exempt 
def publicarTutoria(request): #Esto es para los moviles, no esta terminada
    if request.method == 'POST':
        print("registrando tutoria")
        nombre = request.POST["nombre"]
        
        id_profesor = request.POST["id_profesor"] 
        descripcion = request.POST["descripcion"] 
        
        print(" *** BACK ***"+nombre+"-"+id_profesor+"-"+descripcion)
        #=======================================0
        
        infoFoto=subirFotoTutoria(request)              
        
        dd=[nombre,id_profesor,descripcion,infoFoto]   

        publicarTutoriaMongo(dd)
        #==============================================
        #listaR=json.loads(getTutoriaMongo(id_tutoria))
        return JsonResponse({"ok":"ok"},safe=False)

def subirFotoTutoria(request):
    if request.method == 'POST':
        now = datetime.now()
        #uuid=str(now.microsecond)+str(now.second)+str(now.minute)+str(now.hour)+str(now.day)+str(now.month)+str(now.year)
        myuuid = str(uuid.uuid4())
        
        myfile=request.FILES['Myarchivo']
        fs= FileSystemStorage()
        nombre_archivo=myuuid+str((myfile.name).strip())
        #extension_archivo=str(myfile.name).split(sep='.')[1]
        extension_archivo=str(myfile.name).split(sep='.').pop()
        
        filename=fs.save(nombre_archivo,myfile)
        uploaded_file_url=fs.url(filename)
       
        return {"url":uploaded_file_url,"nombre":nombre_archivo,"extension":extension_archivo}
        #return uploaded_file_url

@csrf_exempt 
def getEntrada(request):
    if request.method == 'POST':
        print("Buscando entrada de la tutoria")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        
        id_entrada=datarecivida['id_entrada']
        current_user_id=datarecivida['current_user_id']
        print(id_entrada)
        listaR=json.loads(getEntradaMongo(id_entrada,current_user_id))
        print(listaR)
        if (str(listaR)=="500"):
            #print("---bk--- 500")
            return JsonResponse({},safe=False,status="500")
        elif (str(listaR)=="403"):
            #print("---bk--- 403")
            return JsonResponse({},safe=False,status="403")
        else:
            #print("---bk--- 200")
            return JsonResponse((listaR),safe=False,status="200")
            #return JsonResponse((listaR),safe=False)

@csrf_exempt 
def registrarEntrada(request):
    if request.method == 'POST':
        print("registrando tutoria")
        titulo = request.POST["titulo"]
        descripcion = request.POST["descripcion"] 
        id_tutoria = request.POST["id_tutoria"] 
        id_profesor = request.POST["id_profesor"] 
        
        current_user_id=request.POST['current_user_id']
        
        print(" *** BACK ***"+titulo+"-"+id_profesor+"-"+descripcion+"->"+current_user_id)
        #=======================================0
        
        urlsArchivos=subirArchivosEntrada(request)          
        data=[id_tutoria,id_profesor,titulo,descripcion,urlsArchivos,current_user_id]
        st=registrarEntradaMongo(data)

        #==============================================
        #listaR=json.loads(getTutoriaMongo(id_tutoria))
        return JsonResponse({"ok":"ok"},safe=False,status=st)

def subirArchivosEntrada(request):
    if request.method == 'POST':

        lita_urls=[]
        a=0
        for file in request.FILES:
            myuuid = str(uuid.uuid4())
            myfile=request.FILES['Myarchivo'+str(a)]
            fs= FileSystemStorage()
            nombre_archivo=myuuid+str((myfile.name).strip())
            #extension_archivo=str(myfile.name).split(sep='.')[1]
            extension_archivo=str(myfile.name).split(sep='.').pop()
            
            filename=fs.save(nombre_archivo,myfile)
            uploaded_file_url=fs.url(filename)
            
            a=a+1

            lita_urls.append({"url":uploaded_file_url,"nombre":nombre_archivo,"extension":extension_archivo})
        
            #return {"url":uploaded_file_url,"extension":str(myfile.name).split(sep='.')[1]}
        return lita_urls

@csrf_exempt 
def registrarEntrada2(request):
    if request.method == 'POST':
        print("registrando entrada")
        ##print(" BACK**** "+str(request.body))
        datarecivida =json.loads(request.body.decode("utf-8")) 
        
        titulo=datarecivida['titulo']
        id_tutoria=datarecivida['id_tutoria']        
        id_profesor=datarecivida['id_profesor'] #ide del usuario que publica la entrada
        descripcion=datarecivida['descripcion']
        
        data=[id_tutoria,id_profesor,titulo,descripcion]

        registrarEntradaMongo(data)
        
        #listaR=json.loads(getTutoriaMongo(id_tutoria))
        return JsonResponse({"ok":"ok"},safe=False)

@csrf_exempt 
def updateEntrada(request):
    if request.method == 'POST':
        print("registrando entrada")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        print("--------------------------------------")
        print("datarecivida: "+str(datarecivida))
        
        titulo=datarecivida['titulo']
        descripcion=datarecivida['descripcion']
        id_entrada=datarecivida['id_entrada']     
        
        
        data=[id_entrada,titulo,descripcion]

        updateEntradaMongo(data)
        
        #listaR=json.loads(getTutoriaMongo(id_tutoria))
        return JsonResponse({"ok":"ok"},safe=False)
    
@csrf_exempt 
def subirArchivotest(request):
    if request.method == 'POST':
        
        myfile=request.FILES['Myarchivo']
        fs= FileSystemStorage()
        filename=fs.save(myfile.name,myfile)
        uploaded_file_url=fs.url(filename)
        print(uploaded_file_url)
        
        print("========================================")
        print(filename)
        print("========================================")
        #print("name: "+filename+",size: "+str(myfile.size)+",extension: "+str(myfile.name).split(sep='.')[1])
        print("************")
        return JsonResponse({"ok":"ok"},safe=False)

@csrf_exempt 
def subirArchivos(request):
    if request.method == 'POST':
        data = request.FILES
        uploadedFiles = data.getlist('myfiles')
        for single_file in uploadedFiles :
            print(single_file)
            fs= FileSystemStorage()
            filename=fs.save(single_file.name,single_file)
            uploaded_file_url=fs.url(filename)
            print(uploaded_file_url)
            
        return HttpResponse("SIIII")
        
    return HttpResponse("No se subio nada")
    
@csrf_exempt 
def getSolicitudesProfesor(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        correo=datarecivida['correo']
        id_usuario=getIdUsuarioMongo(correo)
        
        print("bUSCANDO LAS SOLICITUDES: "+id_usuario )
        listaR=json.loads(getSolicitudesProfesorMongo(id_usuario)) #se convierte a json la cadena que viene en formato json
        return JsonResponse((listaR),safe=False)
    

@csrf_exempt 
def getSolicitudesEstudiante(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        correo=datarecivida['correo']
        id_usuario=getIdUsuarioMongo(correo)
        
        print("bUSCANDO LAS SOLICITUDES: "+id_usuario )
        listaR=json.loads(getSolicitudesEstudianteMongo(id_usuario)) #se convierte a json la cadena que viene en formato json
        return JsonResponse((listaR),safe=False)





@csrf_exempt 
def rechazarSolicitud(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        id_solicitud=datarecivida['id_solicitud']
        id_usuario=datarecivida['id_usuario'] #es el id del usuario(debe ser necesariamente un profesor)  que inicio sesion en el front y es el que manda la peticion, se debe validar que sea el dueño de la tutoria
        
        status= rechazarSolicitudMongo(id_solicitud,id_usuario)
        
        print("estado: "+status)
        
        return JsonResponse({},safe=False,status=status)
    
@csrf_exempt 
def cancelarSolicitud(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        id_solicitud=datarecivida['id_solicitud']
        id_usuario=datarecivida['id_usuario'] #es el id del usuario que inicio sesion en el front y es el que manda la peticion, se debe validar que sea el dueño de la solicitud
        
        status= cancelarSolicitudMongo(id_solicitud,id_usuario)
        
        print("estado: "+status)
        
        return JsonResponse({},safe=False,status=status)
    
@csrf_exempt 
def registrarSolicitud(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        id_tutoria_publicada=datarecivida['id_tutoria_publicada']
        id_solicitante=datarecivida['id_solicitante']
        id_profesor=datarecivida['id_profesor']
        
        status= registrarSolicitudMongo(id_tutoria_publicada,id_solicitante,id_profesor)
        
        #print("estado: "+status)
        
        return JsonResponse({"ok":"ok"},safe=False,status=status)
    
@csrf_exempt     
def aceptarSolicitud(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        id_solicitud=datarecivida['id_solicitud']
        id_usuario=datarecivida['id_usuario'] #es el id del usuario(debe ser necesariamente un profesor) que inicio sesion en el front y es el que manda la peticion, se debe validar que sea el dueño de la tutoria
                
        listaR=json.loads(aceptarSolicitudMongo(id_solicitud,id_usuario))  
        print("*** BACK **** estado: "+str(listaR))
        print("*** BACK **** estado: "+str(listaR[0]))
              
        return JsonResponse(listaR,safe=False,status=listaR[0]['status'])

@csrf_exempt 
def borrarSolicitud(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        id_solicitud=datarecivida['id_solicitud']
        id_usuario=datarecivida['id_usuario'] #es el id del usuario que inicio sesion en el front y es el que manda la peticion, se debe validar que sea el dueño de la solicitud
        
        status= borrarSolicitudMongo(id_solicitud,id_usuario)
        
        print("estado: "+status)
        
        return JsonResponse({},safe=False,status=status)
    
    
    
@csrf_exempt    
def unirmeTutoria(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        id_tutoria=datarecivida['id_tutoria']
        id_usuario=datarecivida['id_usuario'] #es el id del usuario(debe ser necesariamente un profesor) que inicio sesion en el front y es el que manda la peticion, se debe validar que sea el dueño de la tutoria
        
        status= unirmeTutoriaMongo(id_tutoria,id_usuario)
        
        print("estado: "+status)
        
        return JsonResponse({},safe=False,status=status)


#Validaciones    

@csrf_exempt    
def validarPermisoAccesoTutoria(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        id_tutoria=datarecivida['id_tutoria']
        current_user_id=datarecivida['current_user_id'] #es el id del usuario(debe ser necesariamente un profesor) que inicio sesion en el front y es el que manda la peticion, se debe validar que sea el dueño de la tutoria
        if (validarPermisoAccesoTutoriaMongo(id_tutoria,current_user_id)==False): 
            return JsonResponse({"result":False},safe=False,status="403")
        else:
            return JsonResponse({"result":True},safe=False,status="200")
        
@csrf_exempt   
def validarPermisoAccesoEntrada(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        id_entrada=datarecivida['id_entrada']
        current_user_id=datarecivida['current_user_id'] #es el id del usuario(debe ser necesariamente un profesor) que inicio sesion en el front y es el que manda la peticion, se debe validar que sea el dueño de la tutoria
        if (validarPermisoAccesoEntradaMongo(id_entrada,current_user_id)==False): 
            return JsonResponse({"result":False},safe=False,status="403")
        else:
            return JsonResponse({"result":True},safe=False,status="200")
        
        
        

@csrf_exempt 
def finalizarTutoria(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        id_tutoria=datarecivida['id_tutoria']
        id_usuario=datarecivida['id_usuario'] #es el id del usuario que inicio sesion en el front y es el que manda la peticion, se debe validar que sea el dueño de la solicitud
        estrellasTutor=datarecivida['estrellasTutor']
        estrellasTutoria=datarecivida['estrellasTutoria']
        
        status=200;
        status= finalizarTutoriaMongo(id_tutoria,id_usuario)
        print("**** Estado peticion finalizar : "+status)
        
        try:
            calificarMongo(id_tutoria,estrellasTutor,estrellasTutoria);
        except:
            pass
        
        return JsonResponse({},safe=False,status=status)


@csrf_exempt 
def descargarsup(request):
    if request.method == 'GET':
       
 
        filename = '792ef159-4abc-4fe6-8fed-a1a53c2e9c5eVID-20230313-WA0003.mp4'
    
        #filepath = MEDIA_ROOT + '/descargar/archivos/' + filename 
        filepath=os.path.join(MEDIA_ROOT,'792ef159-4abc-4fe6-8fed-a1a53c2e9c5eVID-20230313-WA0003.mp4')
    
        path = open(filepath,'rb')
        print(filepath)
        mime_type, _ = mimetypes.guess_type(filepath)
        
        
        response = HttpResponse(path, content_type = mime_type)
        response['Content-Disposition'] = f"attachment; filename={filename}"
        
        #return HttpResponse("Ruta: "+str(filepath))
        return response


@csrf_exempt 
def descargar(request):
    if request.method == 'GET':
       
        print("OK")
        the_file_name = 'xxx.mp4' # El nombre de archivo de descarga predeterminado que se muestra en el cuadro de diálogo emergente      
        #filename = 'media / uploads / xxx.png' # Ruta del archivo para descargar  
        filename=os.path.join(MEDIA_ROOT,'792ef159-4abc-4fe6-8fed-a1a53c2e9c5eVID-20230313-WA0003.mp4')
        print("ruta "+filename)
        response=StreamingHttpResponse(readFile(filename))  
        response['Content-Type']='application/octet-stream'  
        response['Content-Disposition']='attachment;filename="{0}"'.format(the_file_name)  
        return response 
    

def readFile(filename,chunk_size=512):  
    with open(filename,'rb') as f:  
        while True:  
            c=f.read(chunk_size)  
            if c:  
                yield c  
            else:  
                break 