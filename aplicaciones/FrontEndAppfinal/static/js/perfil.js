function actualizarUsuario(correo){
    nombre=document.getElementById("nombre").value
    telefono=document.getElementById("telefono").value
    direccion=document.getElementById("direccion").value
    descripcion=document.getElementById("descripcion").value
    

    
    if(validarCamposTextVacios([nombre,telefono,direccion,descripcion])){ return 0;}

    data={
        "correo":correo,
        "nombre":nombre,
        "telefono":telefono,
        "direccion":direccion,
        "descripcion":descripcion
    }


    fetch(SERVER_URL+'/api/updateInfoUsuario/'/*'http://localhost:8000/api/registrarSolicitud/'*/,{
        method:'POST',
        body:JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data =>{
            console.log(data)
            location.href = SERVER_URL+"/web/perfil/";
            
        } )
        .catch(function(error) {
            console.log('Hubo un problema con la petición Fetch:' + error.message);
        });
    
    



}

function cambiarFotoPerfil(correo){
    let fd = new FormData();
    fd.append("Myarchivo", document.getElementById("Myarchivo").files[0]);
    fd.append("correo", correo);

    fetch(SERVER_URL+'/api/cambiarFotoPerfilUsuario/',{
        method:'POST',
        body:fd
    })
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        location.href = SERVER_URL+"/web/perfil/"+correo;
    } )
    .catch(function(error) {
        console.log('Hubo un problema con la petición Fetch:' + error.message);
      });
   
    

    
}