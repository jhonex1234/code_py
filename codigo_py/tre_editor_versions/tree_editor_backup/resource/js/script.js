                        /************************************Edition resource tree************************************/

                                                 /************all action button************/

$(document).ready(function(){
    $('#createn_tree_edi').click(function(event) {
        var namedoc = document.forms[0].n_tree_edi.value;
        makenewfile(namedoc);
        return false;
    });

});

$(document).ready(function(){
    $('#add_clave_tree_state').click(function(event){
        var namedoc = document.forms[0].n_tree_edi.value;
        var va_l = document.forms[0].clave_tree_edi.value;
        insertState(namedoc,va_l);
    });

});




                                                 /************end action button************/

                                             /************all function ctr************/
function makenewfile(namedoc){
    if (namedoc.length != ''){
        createfilenew(1,namedoc);
    }else {
        alert('!No se pudo Completar accion¡');
    }
}

function insertState(namedoc,va_l){
    if(namedoc.length != ''){
        if(va_l.length != ''){
            makeState(2,namedoc,va_l);
        }else{
            alert('No se pudo completar la accion, campo nombre estado no debe ser nulo');
        }
    }else{
        alert('No se pudo completar la accion, campo nombre documento no debe ser nulo');

    }
}

function addOptions(domElement, array) {
 var select = document.getElementsByName(domElement)[0];
 for (value in array) {
      var option = document.createElement("option");
      option.text = array[value];
      select.add(option);
 }
}

                                                /************End all function ctr************/
                                                
                                                  /************all function send************/
function createfilenew(opc,namedoc){
     $.ajax({
        url: 'process.php',
        dataType: 'json',
        data: {"opc":opc, "namedoc":namedoc}
       
    }).done(function(data){   
        if(data != null){        
            if (data.error != '') {
               alert(data.error);
               return data;
           }
            array = data.result;
            document.forms[0].n_tree_edi.value = data.doc_name;
        }else{
           alert('no se obtuvo datos');
        } 
    }).fail(function(){
        alert(';(');
    });
}

function makeState(opc,namedoc,val) {
    $.ajax({
        url: 'process.php',
        dataType: 'json',
        data:{"opc":opc,"namedoc":namedoc,"val":val}

    }).done(function(data){
        if(data != null){        
            if (data.error != '') {
               alert(data.error);
               return data;
           }
            array = data.result;
            if(data.msj != null){
                alert(data.msj);
            }else{
            $('#llstate_selec').find('option').remove();
            document.forms[0].n_tree_edi.value = '';
            document.forms[0].n_tree_edi.value = data.doc_name;
            addOptions('llstate_selec', array)
        
            }    
        }else{
           alert('no se obtuvo datos');
        }
    }).fail(function(){
        alert('Error Linea code-(1)');
    });
}
                                           /************all function send************/
               /************************************Edition resource tree************************************/
                                        