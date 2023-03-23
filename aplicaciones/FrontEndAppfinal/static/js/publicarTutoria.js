
function publicarTutoria(){
    titulo=document.getElementById("txbtitulo").value
    descripcion=document.getElementById("txbdescripcion").value
    id_profesor=document.getElementById("id_profesor").value
    
    let fd = new FormData();
    
    if(validarCamposTextVacios([titulo,descripcion,id_profesor])){ return 0;}
    if(validarCampoArchivos(document.getElementById("Myarchivo").files.length)){ return 0;}

    fd.append("nombre", titulo);
    fd.append("descripcion", descripcion);
    fd.append("id_profesor", id_profesor);
    fd.append("Myarchivo", document.getElementById("Myarchivo").files[0]);


    //print(document.getElementById("Myarchivo").files)
    
    fetch(SERVER_URL+'/api/publicarTutoria/',{
        method:'POST',
        body:fd
    })
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        location.href = SERVER_URL+"/web/getCatalogoTutorias/";
    } )
    .catch(function(error) {
        console.log('Hubo un problema con la petición Fetch:' + error.message);
      });
   
    
}

function validarCamposTextVacios(campos){
    r=false
    campos.forEach(campo => {
        if (campo == null || campo=="" || campo.length<=0){
            alert("Debe llenar Todos los campos");
            r=true;
            return r;
        }
    });
    return r;
}

function validarCampoArchivos(a){
    r=false
    if(a<=0){
        alert("Debes seleccionar un archivo");
        r=true;
        return r;
    }
    return r;
}