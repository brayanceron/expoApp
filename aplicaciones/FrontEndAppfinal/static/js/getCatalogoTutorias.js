
function btnInscribir(id_solicitante,id_tutoria,id_profesor){
  //alert(id_solicitante+"ok"+id_tutoria+"ok"+id_profesor)
 
  fetch(SERVER_URL+'/api/registrarSolicitud/'/*'http://localhost:8000/api/registrarSolicitud/'*/,{
      method:'POST',
      body:JSON.stringify({
          "id_solicitante":id_solicitante,
          "id_tutoria_publicada":id_tutoria,
          "id_profesor":id_profesor
      }),
      /*
      'mode': 'no-cors',
	  'headers': {
            'Access-Control-Allow-Origin': '*',
        }*/

  })
  .then(response => response.json())
  .then(data =>{
      console.log(data)
      //location.href = SERVER_URL+"/web/getMisTutorias/";
      location.href = SERVER_URL+"/web/getSolicitudes/";
      
  } )
  .catch(function(error) {
      console.log('Hubo un problema con la petición Fetch:' + error.message);
    });

  

}

