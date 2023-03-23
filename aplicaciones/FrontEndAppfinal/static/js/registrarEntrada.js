
function registrarEntrada(current_user_id){
   
    titulo=document.getElementById("txbtitulo").value
    descripcion=document.getElementById("txbdescripcion").value
    id_tutoria=document.getElementById("id_tutoria").value
    id_profesor=document.getElementById("id_profesor").value

    if(validarCamposTextVacios([titulo,descripcion,id_profesor,id_tutoria])){ return 0;}

    let fd = new FormData();
    
    fd.append("titulo", titulo);
    fd.append("descripcion", descripcion);
    fd.append("id_tutoria", id_tutoria);
    fd.append("id_profesor", id_profesor);
    fd.append("current_user_id", current_user_id);

    //fd.append("Myarchivo", document.getElementById("Myarchivo").files[0]);
    a=0
    for (file in document.getElementById("Myarchivo").files){
        fd.append("Myarchivo"+a, document.getElementById("Myarchivo").files[a]);
        a++
    }
    //array1.forEach(element => console.log(element));

    //fd.append("Myarchivo", document.getElementById("Myarchivo").files);

    console.log(document.getElementById("Myarchivo").files)
    console.log("------------------------")

    fetch(SERVER_URL+'/api/registrarEntrada/',{
        method:'POST',
        body:fd
    })
    .then(response => {
        console.log("respuesta: "+response.status)
        console.log(typeof response.status)
        if(response.status.toString()=="500"){
            alert("Error en el servidor")
            return "Error en el servidor"
        }
        else if(response.status.toString()=="403"){
            alert("No autorizado")
            return "No autorizado"
        }
        else{
            return response.json();
        }
        
    })
    .then(data =>{
        console.log(data)
        location.href = SERVER_URL+"/web/getContenidoTutoria/"+id_tutoria+"";
    } )
    .catch(function(error) {
        console.log('Hubo un problema con la petición Fetch:' + error.message);
      });

}


function registrarEntrada2(){
   
    titulo=document.getElementById("txbtitulo").value
    descripcion=document.getElementById("txbdescripcion").value
    id_tutoria=document.getElementById("id_tutoria").value
    id_profesor=document.getElementById("id_profesor").value

    fetch('http://localhost:8000/api/registrarEntrada/',{
        method:'POST',
        body:JSON.stringify({
            "titulo":titulo,
            "descripcion":descripcion,
            "id_tutoria":id_tutoria,
            "id_profesor":id_profesor
        })
    })
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        location.href = "http://localhost:8000/web/getContenidoTutoria/"+id_tutoria;
    } )
    .catch(function(error) {
        console.log('Hubo un problema con la petición Fetch:' + error.message);
      });

    
}




