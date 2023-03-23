 const SERVER_URL="http://192.168.1.57:8000"
 
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


 const Myvariable="BRAYANCERON";