                                                 /************all action button************/

$(document).ready(function(){
    $('#createn_tree_edi').click(function(event) {

        namedoc = document.forms[0].n_tree_edi.value;
        alert(namedoc);
        return false;
        //makenewfile(namedoc);
    });
});
                                                 /************end eyelash nuevo************/


                                                 /************all function send************/
function createfilenew(opc,namedoc,keyvalue,message){
     $.ajax({
        url: 'process.php',
        dataType: 'json',
        data: {"opc":opc, "namedoc":namedoc,"keyvalue":keyvalue,"message":message}
       
    }).done(function(data){   
        if(data != null){        
            if (data.error != '') {
               alert(data.error);
               return data;
           }
        array = data.result;
        document.forms[0].newname.value = data.doc_name;
        $('#listnewkey').find('option').remove();
        addOptions("listnewkey", array);
        document.getElementById("newfilej").disabled=true
        document.getElementById("newname").disabled=true
        }else{
           alert('no se obtuvo datos');
        }        
    }).fail(function(){
        alert(';(');
    });
                                            /************eyelash nuevo***********/
                                                
                                                 /************all function ctr************/
function makenewfile(namedoc,keyvalue,message){
    if (namedoc.length != ''){
        if(keyvalue.trim() != ''){
            if(message.trim() != ''){
               createfilenew(7,namedoc,keyvalue,message);
            }else{
             alert('te falta el campo mensaje');    
            }
        }else{
            alert('te falta el campo clave');    
        } 
    }else {
        alert('te falta el campo nombre documeto');
    }
 }
}