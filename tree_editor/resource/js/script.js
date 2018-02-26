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

}
                                                 /************all action button************/

$(document).ready(function(){
    $('#newfilej').click(function(event) {
        namedoc = document.forms[0].newname.value;
        keyvalue = document.forms[0].newkeyvalue.value;
        message = document.forms[0].newtem.value;
        makenewfile(namedoc,keyvalue,message);
    });
});
                                                 /************end eyelash nuevo************/

