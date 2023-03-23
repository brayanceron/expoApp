
function actualizarTutoriaPublicada(correo,id_tutoria){
    nombre=document.getElementById("nombre").value
    descripcion=document.getElementById("descripcion").value
    
    if(validarCamposTextVacios([nombre,descripcion])){ return 0;}

    data={
        "correo":correo,
        "nombre":nombre,
        "descripcion":descripcion,
        "id_tutoria":id_tutoria
    }


    fetch(SERVER_URL+'/api/updateTutoriaPublicada/'/*'http://localhost:8000/api/registrarSolicitud/'*/,{
        method:'POST',
        body:JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data =>{
            console.log(data)
            location.href = SERVER_URL+"/web/getTutoriaPublicada/"+id_tutoria;
            
        } )
        .catch(function(error) {
            console.log('Hubo un problema con la petición Fetch:' + error.message);
        });
    
    
    
    


}

function cambiarFotoPerfilTutoria(id_tutoria){
    
    let fd = new FormData();
    fd.append("Myarchivo", document.getElementById("Myarchivo").files[0]);
    fd.append("id_tutoria", id_tutoria);

    fetch(SERVER_URL+'/api/cambiarFotoPerfilTutoria/',{
        method:'POST',
        body:fd
    })
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        location.href = SERVER_URL+"/web/getTutoriaPublicada/"+id_tutoria;
    } )
    .catch(function(error) {
        console.log('Hubo un problema con la petición Fetch:' + error.message);
      });
   
    
    
}