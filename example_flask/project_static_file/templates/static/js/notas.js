$(window).unload(function () {
   $.ajax({
     type: 'GET',
     async: false,
     url: 'SomeUrl.com?id=123'
   });
});


var _wasPageCleanedUp = false;
function pageCleanup()
{
    if (!_wasPageCleanedUp)
    {
        $.ajax({
            type: 'GET',
            async: false,
            url: 'SomeUrl.com/PageCleanup?id=123',
            success: function ()
            {
                _wasPageCleanedUp = true;
            }
        });
    }
}


$(window).on('beforeunload', function ()
{
    //this will work only for Chrome
    pageCleanup();
});

$(window).on("unload", function ()
{
    //this will work for other browsers
    pageCleanup();
});



var bPreguntar = true;
 
  window.onbeforeunload = preguntarAntesDeSalir;
 
  function preguntarAntesDeSalir () {
    var respuesta;
 
    if ( bPreguntar ) {
      respuesta = confirm ( '¿Seguro que quieres salir?' );
 
      if ( respuesta ) {
        window.onunload = function () {
          
          return true;
        }
      } else {
         return false;
      }
    }
  }














$.$.post("../../componentes/controlador/controlado_prueba.php",function(){
      $("#resultado").html(datos);
  });  
 



///fun 1
function loadOut()
{
       window.location="http://www.google.com";
}


///fun 2
Con ajax.
window.addEventListener("beforeunload", function (e) { 
var nom_persona = window.sessionStorage.getItem('usuario');
$.ajax({
type: "GET",
//callbackParameter:'callback',
dataType:'jsonp',   
jsonp: 'callback',
url:'url',
data:"parametros"});
return;
});

///fun 3
window.onbeforeunload = function(){
    $.ajax({
        type: "POST",
        url: "salida.jsp",
        dataType:"json",
        data: {},
        async : false,
        success : function(){
            }
    });
}

/// fun 4
window.addEventListener("beforeunload", function (e) {
  var confirmationMessage = "\o/";
  (e || window.event).returnValue = confirmationMessage; //Gecko + IE
  return confirmationMessage;                            //Webkit, Safari, Chrome
});

/// fun 5
window.onbeforeunload = confirmExit;
function confirmExit()
{
  return "Ha intentado salir de esta pagina. Si ha realizado algun cambio en los campos sin hacer clic en el boton Guardar, los cambios se perderan. Seguro que desea salir de esta pagina? ";
}

/// fun 6
window.onbeforeunload = function(t){
 t.returnValue="Saliendo..";
 return confirm("Seguro deseas salir?")
};

/// fun 7
  var bPreguntar = true;
 
  window.onbeforeunload = preguntarAntesDeSalir;
 
  function preguntarAntesDeSalir () {
    var respuesta;
 
    if ( bPreguntar ) {
      respuesta = confirm ( '¿Seguro que quieres salir?' );
 
      if ( respuesta ) {
        window.onunload = function () {
          return true;
        }
      } else {
        return false;
      }
    }
  }

/// fun 8
function adios() {
     alert('adios, regresa pronto');


function(){
    $.ajax({
        type: "POST",
        url: "componentes/controlador/controlado_prueba.php",
        dataType:"json",
        data: {},
        async : false,
        success : function(){
            }
    }).fail(function(){alert("no lo tomo")});
}


function initialize(date){
    $("ul").empty();
    $.ajax({
        url: "process.php",
        data: {"sessionId" : sessionId, "activateId" : "true", "message" : ""},
        dataType: "json"
    }).fail(function() {
        alert("Oops... an error occurred");
    }); 
}


  window.onbeforeunload = alert("carga");
  
  function initialize(date){
    $("ul").empty();
    $.ajax({
        url: "process.php",
        data: {"sessionId" : sessionId, "activateId" : "true", "message" : ""},
        dataType: "json"
    }).fail(function() {
        alert("Oops... an error occurred");
    }); 
}
