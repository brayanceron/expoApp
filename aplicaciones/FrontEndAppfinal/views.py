from django.shortcuts import redirect, render
import requests

from aplicaciones.FrontEndAppfinal.forms import customUserCreationForm
from django.http import HttpResponse
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


SERVER_URL="http://192.168.1.57:8000"
#SERVER_URL="http://localhost:8000"

def getCatalogoTutorias2(request):
    resp = requests.get(SERVER_URL+'/api/getCatalogoTutorias/')   
    
    json_response=resp.json()
        
    return render(request,'getCatalogoTutorias.html',{"json_response":json_response})

def currentuser(request):
    return HttpResponse("usu: "+str(request.user)+" email: "+str(request.user.email))

def getTutoria(request):
    id_tutoria='63e9bc8d811ef54a3de5952c'

    resp = requests.post(SERVER_URL+'/api/getTutoria/',json={'id_tutoria':id_tutoria})   
    json_response=resp.json()

    #print("***** FRONT *****"+str(json_response))
    
    return render(request,'getTutoria.html',{"json_response":json_response})

def getMisTutorias2(request):
    correo=request.user.email
    tutorias_estudiante = requests.post(SERVER_URL+'/api/getMisTutoriasEnProgresoEstudiante/',json={'correo':correo}).json()
    tutorias_profesor = requests.post(SERVER_URL+'/api/getMisTutoriasEnProgresoProfesor/',json={'correo':correo}).json()
    tutorias_publicadas = requests.post(SERVER_URL+'/api/getMisTutoriasPublicadas/',json={'correo':correo}).json()
    
    a=0
    for t in tutorias_profesor:
        tutorias_profesor[a]["idn"]=t['_id']['$oid']
        tutorias_profesor[a]["id_profesorn"]=t['id_profesor'][0]['_id']['$oid']
        a=a+1

    
    return render(request,'getMisTutorias.html',
                  {"tutorias_estudiante":tutorias_estudiante,
                   'tutorias_profesor':tutorias_profesor,
                   'tutorias_publicadas':tutorias_publicadas})

def getContenidoTutoria2(request,id_tutoria):
    if request.method == 'GET':
               
        contenido_tutoria = requests.post(SERVER_URL+'/api/getContenidoTutoria/',json={'id_tutoria':id_tutoria}).json()
        info_tutoria = requests.post(SERVER_URL+'/api/getTutoria/',json={'id_tutoria':id_tutoria}).json()
        #validar que pasa cuando la lista es vacia(PASO LO MISMO CON LA APP MOVIL)
        #contenido_tutoria[0]['id_tutoria']=contenido_tutoria[0]['id_tutoria']['$oid']
        info_tutoria[0]['id_tutoria']=info_tutoria[0]['_id']['$oid']
        info_tutoria[0]['nombre_profesor']=info_tutoria[0]['id_profesor'][0]['nombre']
        info_tutoria[0]['id_profesor']=info_tutoria[0]['id_profesor'][0]['_id']['$oid']
        
        
        return render(request,'getContenidoTutoria.html',{"contenido_tutoria":contenido_tutoria,"info_tutoria":info_tutoria})
    


def registrarEntrada2(request,id_tutoria,id_profesor):
    #id_tutoria = request.POST["id_tutoria"]
    #id_profesor = request.POST["id_profesor"]
    
    #titulo=datarecivida['titulo']
    #id_tutoria=datarecivida['id_tutoria']        
    #id_profesor=datarecivida['id_profesor']
    #descripcion=datarecivida['descripcion']
    
    return render(request,'registrarEntrada.html',{"id_tutoria":id_tutoria,"id_profesor":id_profesor})


def publicarTutoria2(request,id_profesor):
    return render(request,'publicarTutoria.html',{'id_profesor':id_profesor})




def signin(request):
    if(request.user.is_authenticated ): return redirect(to="getCatalogoTutorias")
    
    data={
        'form':customUserCreationForm
    }
    error="_"
    
    if(request.method=='POST'):
        
        formulario=customUserCreationForm(data=request.POST)
        print("****FRONT***")
        #print(formulario.cleaned_data["username"])
        #print(formulario.cleaned_data["password1"])
        if formulario.is_valid():
            print("****FRONT***")
            print(formulario.cleaned_data["username"])
            print(formulario.cleaned_data["password1"])
                        
            userdata={
                "correo":formulario.cleaned_data["email"],
                "rol":request.POST["rol"],
                "nombre":formulario.cleaned_data["first_name"]+" "+formulario.cleaned_data["last_name"]
            }
            
            print(userdata)
            
            peticion=requests.post(SERVER_URL+'/api/registrarUsuario/',json=userdata)
            
            if(str(peticion.status_code)=="428"):    print("**FRONT**428"); error = "Ya Existe un usuario con ese correo"            
            elif (str(peticion.status_code)=="500"): print("**FRONT**500"); error= "Error en el servido, no se pudó completar la solicitud"
            elif (str(peticion.status_code)=="200"): 
                print("**FRONT**200");           
                formulario.save()
                #Ojo aqui hay que registrar el usuario en labase de datos de mongo
                user=authenticate(username=formulario.cleaned_data["email"],password=formulario.cleaned_data["password1"])
                login(request,user)
                return redirect(to="getCatalogoTutorias")
        else: 
            error="Error Al validar los campos del formulario"
        data["form"]=formulario
        
        #--------------------------------------------------
        #formulario=customUserCreationForm(data=request.POST)
        #if formulario.is_valid():
        #    formulario.save()
        #    #Ojo aqui hay que registrar el usuario en labase de datos de mongo y en la firebase tambien
        #    user=authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
        #    login(request,user)
            
        #    return redirect(to="getCatalogoTutorias")
        #data["form"]=formulario
    
    return render(request,'signin.html',{"form":data['form'],"error":error})


#--------------------------------------------------------------------------------------
@login_required
def getCatalogoTutorias(request):
    correo=request.user.email
    json_response = requests.get(SERVER_URL+'/api/getCatalogoTutorias/').json()
    info_usuario= getInfoUsuario(correo)
    #json_response=resp
    a=0
    for t in json_response:
        print("**FRONT "+str(a))
        print(t)
        json_response[a]["idn"]=t['_id']['$oid']    #id de la tutoria publicada
        json_response[a]["id_profesorn"]=t['id_profesor'][0]['_id']['$oid']
        a=a+1
    return render(request,'getCatalogoTutorias.html',{"json_response":json_response,"info_usuario":info_usuario})

@login_required
def getMisTutorias(request):
    correo=request.user.email
    info_usuario= getInfoUsuario(correo)
    tutorias_estudiante = requests.post(SERVER_URL+'/api/getMisTutoriasEnProgresoEstudiante/',json={'correo':correo}).json()
    tutorias_profesor = requests.post(SERVER_URL+'/api/getMisTutoriasEnProgresoProfesor/',json={'correo':correo}).json()
    tutorias_publicadas = requests.post(SERVER_URL+'/api/getMisTutoriasPublicadas/',json={'correo':correo}).json()
    
    a=0
    for t in tutorias_profesor:
        tutorias_profesor[a]["idn"]=t['_id']['$oid']
        tutorias_profesor[a]["id_profesorn"]=t['id_profesor'][0]['_id']['$oid']
        a=a+1
        
    b=0
    for t in tutorias_estudiante:
        tutorias_estudiante[b]["idn"]=t['_id']['$oid']
        #tutorias_estudiante[b]["id_profesorn"]=t['id_profesor'][0]['_id']['$oid']
        b=b+1
    c=0
    for t in tutorias_publicadas:
        tutorias_publicadas[c]["idn"]=t['_id']['$oid']
        #tutorias_estudiante[b]["id_profesorn"]=t['id_profesor'][0]['_id']['$oid']
        c=c+1
    

    
    return render(request,'getMisTutorias.html',
                  {"tutorias_estudiante":tutorias_estudiante,
                   'tutorias_profesor':tutorias_profesor,
                   'tutorias_publicadas':tutorias_publicadas,"info_usuario":info_usuario})

@login_required
def getContenidoTutoria(request,id_tutoria):
    if request.method == 'GET':
        correo=request.user.email
        info_usuario= getInfoUsuario(correo)
        current_user_id=info_usuario[0]["id_usuario_actual"]

        peticion=requests.post(SERVER_URL+'/api/getContenidoTutoria/',json={'id_tutoria':id_tutoria,"current_user_id":current_user_id})
        print("***FRONT*** "+str(peticion.status_code))
        
        if (str(peticion.status_code)=="403"): return HttpResponse("Acceso no autorizado")
        if (str(peticion.status_code)=="500"): return HttpResponse("Error en el servido, no se pudó completar la solicitud")
        
        contenido_tutoria=peticion.json()
        
        
        a=0
        for tutoria in contenido_tutoria:
            contenido_tutoria[a]["idn"]=tutoria["_id"]["$oid"]
            a=a+1
        
        info_tutoria = requests.post(SERVER_URL+'/api/getTutoria/',json={'id_tutoria':id_tutoria}).json()
        #validar que pasa cuando la lista es vacia(PASO LO MISMO CON LA APP MOVIL)
        #contenido_tutoria[0]['id_tutoria']=contenido_tutoria[0]['id_tutoria']['$oid']
        info_tutoria[0]['id_tutoria']=info_tutoria[0]['_id']['$oid']
        info_tutoria[0]['nombre_profesor']=info_tutoria[0]['id_profesor'][0]['nombre']
        info_tutoria[0]['id_profesor']=info_tutoria[0]['id_profesor'][0]['_id']['$oid']
        
        
        return render(request,'getContenidoTutoria.html',{"contenido_tutoria":contenido_tutoria,"info_tutoria":info_tutoria,"info_usuario":info_usuario})
        #return render(request,'getContenidoTutoria.html',{"contenido_tutoria":contenido_tutoria,"info_tutoria":info_tutoria})






@login_required
def publicarTutoria(request,id_profesor):
    correo=request.user.email
    info_usuario= getInfoUsuario(correo)
    return render(request,'publicarTutoria.html',{'id_profesor':id_profesor,"info_usuario":info_usuario})

@login_required
def getEntrada(request,id_entrada):
    correo=request.user.email
    info_usuario= getInfoUsuario(correo)
    #print("***FRONT***")
    #print(info_usuario[0]["id_usuario_actual"])
    
    peticionPermiso=requests.post(SERVER_URL+'/api/validarPermisoAccesoEntrada/',json={'id_entrada':id_entrada,"current_user_id":info_usuario[0]["id_usuario_actual"]})
    if(str(peticionPermiso.status_code)=="403"): return HttpResponse("Acceso no autorizado")
    
    peticion=requests.post(SERVER_URL+'/api/getEntrada/',json={'id_entrada':id_entrada,"current_user_id":info_usuario[0]["id_usuario_actual"]})
    #if (str(peticion.status_code)=="403"): return HttpResponse("Acceso no autorizado")
    if (str(peticion.status_code)=="500"): return HttpResponse("Error en el servido, no se pudó completar la solicitud")
    
    
    
    contenido_entrada = peticion.json()
    return render(request,'getEntrada.html',{"contenido_entrada":contenido_entrada,"info_usuario":info_usuario})
    #return HttpResponse("prueba")

@login_required
def registrarEntrada(request,id_tutoria):
    correo=request.user.email
    #info_usuario = requests.post(SERVER_URL+'/api/getInfoUsuario/',json={'correo':correo}).json()
    #info_usuario[0]["id_usuario_actual"]=info_usuario[0]["_id"]["$oid"]
    info_usuario= getInfoUsuario(correo)
    
    peticion=requests.post(SERVER_URL+'/api/validarPermisoAccesoTutoria/',json={'id_tutoria':id_tutoria,"current_user_id":info_usuario[0]["id_usuario_actual"]})
    if(str(peticion.status_code)=="403"): return HttpResponse("Acceso no autorizado")
    
    
    return render(request,'registrarEntrada.html',{"id_tutoria":id_tutoria,"id_usuario_actual":info_usuario[0]["id_usuario_actual"],"info_usuario":info_usuario})

@login_required
def getSolicitudes(request):
    correo=request.user.email
    solicitudes_estudiante = requests.post(SERVER_URL+'/api/getSolicitudesEstudiante/',json={'correo':correo}).json()
    a=0
    for t in solicitudes_estudiante:
        solicitudes_estudiante[a]["idn"]=t['_id']['$oid']    #id de la solicitud
        a=a+1
    
    solicitudes_profesor = requests.post(SERVER_URL+'/api/getSolicitudesProfesor/',json={'correo':correo}).json()
    b=0
    for t in solicitudes_profesor:
        solicitudes_profesor[b]["idn"]=t['_id']['$oid']    #id de la solicitud
        b=b+1
    
    info_usuario = requests.post(SERVER_URL+'/api/getInfoUsuario/',json={'correo':correo}).json()
    info_usuario[0]["id_usuario_actual"]=info_usuario[0]["_id"]["$oid"]
    
    return render(request,'getSolicitudes.html',{"solicitudes_estudiante":solicitudes_estudiante,"solicitudes_profesor":solicitudes_profesor,"info_usuario":info_usuario})



def getInfoUsuario(correo):
    info_usuario = requests.post(SERVER_URL+'/api/getInfoUsuario/',json={'correo':correo}).json()
    info_usuario[0]["id_usuario_actual"]=info_usuario[0]["_id"]["$oid"]
    return info_usuario
    

   
@login_required
def perfil(request,correo):
    #correo=request.user.email
    info_usuario= getInfoUsuario(correo)
    
    return render(request,'perfil.html',{'info_usuario':info_usuario})

@login_required
def getTutoriaPublicada(request,id_tutoria):
    correo=request.user.email
    info_usuario= getInfoUsuario(correo)
    json_response = requests.post(SERVER_URL+'/api/getTutoriaPublicada/',json={'id_tutoria':id_tutoria}).json()


    return render(request,'getTutoriaPublicada.html',{"json_response":json_response,"id_tutoria":id_tutoria,"info_usuario":info_usuario})
    
    
def handler404(request, template_name='404.html'):
  #from django.shortcuts import render
  return render(request, '404.html')

##METODOS DE LA RESPUESTA
#print(resp)
#print("***** FRONT *****"+str(resp))
#print("***** FRONT *****"+str(resp.json()))
#print("***** FRONT *****"+str(resp.status_code))
#print("***** FRONT *****"+str(resp.text))
#print("***** FRONT *****"+str(resp.content))

#ACCEDER A LA INFORMACION(JSON) DE LA RESPUESTA
#print("***** FRONT ***** "+str(json_response[0]['nombre']))