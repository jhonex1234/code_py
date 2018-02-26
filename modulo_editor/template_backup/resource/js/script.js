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

 function savedicvalue(doc_name,key_value,template){
    if(doc_name.trim() != ''){
            if(keyvalue.trim() != ''){
                if(template.trim() != ''){
                        sendvalues_addnewlist(5,doc_name,key_value,template);      
                }else{
                    alert('te falta el campo edicion template');   
                }
            }else{
                alert('te falta el campo clave');   
                
            }
        }else{
            alert('te falta el campo ruta archivo');   
                
        }
}

function downloadnewfile(namedoc){
    name_doc = document.forms[0].newname.value;
    keyvalue = document.forms[0].newkeyvalue.value;
    template = document.forms[0].newtem.value;
    if(name_doc.trim() != ''){
        if(keyvalue.trim() != ''){
            if(template.trim() != ''){
                document.location.href = "uploads/"+namedoc;
            }else{
                    alert('te falta el campo edicion template');   
            }
        }else{
                alert('te falta el campo clave');   
        }
    }else{
            alert('te falta el campo ruta archivo');   
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
function sendvalues_addnewlist(opc,namedoc,keyvalue,message){
     $.ajax({
        url: 'process.php',
        dataType: 'json',
        data: {"opc":opc, "namedoc":namedoc,"keyvalue":keyvalue,"message":message}
       
    }).done(function(data){   
        if(data != null){        
            if (data.error != '') {
               alert(data.error);
               return data;            }
        array = data.result;
        $('#listnewkey').find('option').remove();
        addOptions("listnewkey", array);
        }else{
           alert('no se obtuvo datos');
        }        
    }).fail(function(){
        alert(';(');
    });
}

/*return list key into file json post load*/
function sendvalues_keys(opc,namedoc,keyvalue){
    $.ajax({
        url: 'process.php',
        dataType: 'json',
        data: {"opc":opc, "namedoc":namedoc,"keyvalue":keyvalue}
       
    }).done(function(data){
        if(data != null){
            if (data.error != '') {
               alert(data.error);
               return data;
            }
            document.forms[0].newtem.value = data.msj;
            
        }else{
            error = 'no se obtuvo datos';
            document.forms[0].edittemp.value = error;
            return true;
        }
    }).fail(function() {
        alert(';( error (1)');
    });
}

function downloadDataUrlFromJavascript(filename){

    // Construct the a element
    var link = document.createElement("a");
    link.download = filename;
    link.target = "_blank";

    // Construct the uri
    link.href = "uploads/";
    document.body.appendChild(link);
    link.click();

    // Cleanup the DOM
    document.body.removeChild(link);
    delete link;
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
$(document).ready(function() {
    $('#savenewkey').click(function(event){
        doc_name = document.forms[0].newname.value;
        key_value = document.forms[0].newkeyvalue.value;
        template = document.forms[0].newtem.value;
        savedicvalue(doc_name,key_value,template);
    });   
});

$(document).ready(function() {
    $('#downfilen').click(function(event){
        namedoc = document.forms[0].newname.value;
        downloadnewfile(namedoc);
    });
});
function load_key(keyvalue){
    document.forms[0].editkeyvalue.value = keyvalue;
    dirfield = document.forms[0].newname.value;
    sendvalues_keys(3,dirfield,keyvalue);
    return true;
}
                                                 /************end eyelash nuevo************/



                                                /************eyelash editar***********/

                                                 /**********all function ctr*******/
function enableinputkeyvalue(value){
    if(value==true)
    {
        // enable
        document.getElementById("editkeyvalue").disabled=false;
    }else if(value==false){
        // disable
        document.getElementById("editkeyvalue").disabled=true;
    }
}

/*delete with keyvalue*/
function deletScrit(namedoc,keyvalue){
    var docVal = $('#docinput').val(); 
    if(docVal != ''){
        document.forms[0].edittemp.value = '';
        if (namedoc.length != ''){
           sendvalues_dele(4,namedoc,keyvalue);
           document.getElementById("editkeyvalue").disabled=false; 
           document.forms[0].editkeyvalue.value = '';
        }else {
            alert('te falta el campo nombre documeto');
        }
    }else{
        alert('se requiere documento para esta acción');
    }
    return true;
}

/*send  key to input id="keyvalue" and
load template with keyvalue*/

function loadkey(keyvalue){
    document.forms[0].editkeyvalue.value = keyvalue;
    dirfield = document.getElementById("docinput").files[0].name;
    sendvalueskeys(3,dirfield,keyvalue);
    return true;
}
// Rutina para agregar opciones a un <select>
function addOptions(domElement, array) {
 var select = document.getElementsByName(domElement)[0];
 for (value in array) {
  var option = document.createElement("option");
  option.text = array[value];
  select.add(option);
 }
}

/*create new json file*/
function createJson(){
    var docVal = $('#docinput').val(); 
    if(docVal != ''){
        keyvalue = document.forms[0].editkeyvalue.value; 
        message = document.forms[0].edittemp.value; 
        namedoc =  document.getElementById("docinput").files[0].name;           
        if (namedoc.length != ''){
            if(keyvalue.trim() != ''){
                if(message.trim() != ''){
                    sendvalues_addlist(5,namedoc,keyvalue,message)
                 }else{
                 alert('te falta el campo mensaje');    
                }
            }else{
                alert('te falta el campo clave');    
            } 
        }else {
            alert('te falta el campo nombre documeto');
        }
    }else{
        alert('se requiere documento para esta acción');
    }
    return true;
}

function editjson(dirField,keyvalue,selctkey,editemplate){
    var docVal = $('#docinput').val(); 
    if(docVal != ''){
        if(dirField.trim() != ''){
            if(keyvalue.trim() != ''){
                if(editemplate.trim() != ''){
                        sendvaluesedit(6,dirField,keyvalue,selctkey,editemplate);      
                }else{
                    alert('te falta el campo edicion template');   
                }
            }else{
                alert('te falta el campo clave');   
                
            }
        }else{
        alert('se requiere documento para esta acción');   
        }
    }else{
        alert('')
    }
}

function downloadfile(namedoc){
    document.location = "uploads/"+namedoc;
}
                                                 /************all function send************/

/*send value for delete*/
function sendvalues_dele(opc,namedoc,keyvalue){
    $.ajax({
    
        url: 'process.php',
        dataType: 'json',
        data: {"opc":opc, "namedoc":namedoc,"keyvalue":keyvalue}

    }).done(function(data){   
        if(data != null){        
            if (data.error != '') {
               alert(data.error);
               return data;
           }
        array = data.result;    
        $('#editkeylist').find('option').remove();
        addOptions("editkeylist", array);
        }else{
           alert('no se obtuvo datos');
        }        
    }).fail(function(){
        alert(';(');
    });
}
/*return list key into file json post load*/
function sendvalueskeys(opc,namedoc,keyvalue){
    $.ajax({
        url: 'process.php',
        dataType: 'json',
        data: {"opc":opc, "namedoc":namedoc,"keyvalue":keyvalue}
       
    }).done(function(data){
        if(data != null){
            if (data.error != '') {
               alert(data.error);
               return data;
            }
             var menssage = data.msj;
            document.forms[0].edittemp.value = menssage.join('<>');
            document.getElementById("editkeyvalue").disabled=true
          
        }else{
            error = 'no se obtuvo datos';
            document.forms[0].edittemp.value = error;
            return true;
        }
    }).fail(function() {
        alert(';( error (1)');
    });
}
/*send name file, while*/
function sendvalues(opc,namedoc){
    var doc = namedoc;
    $.ajax({
        url: 'process.php',
        dataType: 'json',
        data: {"opc":opc, "namedoc":namedoc}
       
    }).done(function(data){
        if(data != null){
            if (data.error != '') {
               alert(data.error);
               return;
            }
        array = data.result;
        doc = data.doc_name;
        $('#editkeylist').find('option').remove();
        addOptions("editkeylist", array);
        }else{
            alert('no se obtuvo datos');
        }
    }).fail(function() {
        alert(';( error (1)');
    });
}

function sendvaluesedit(opc,namedoc,keyvalue,selectkey,message){
    $.ajax({
        url: 'process.php',
        dataType: 'json',
        data: {"opc":opc, "namedoc":namedoc,"keyvalue":keyvalue,"selectkey":selectkey,"message":message}
       
    }).done(function(data){   
        if(data != null){        
            if (data.error != '') {
               alert(data.error);
               return data;
           }
        array = data.result;
        $('#editkeylist').find('option').remove();
        addOptions("editkeylist", array);
        }else{
           alert('no se obtuvo datos');
        }        
    }).fail(function(){
        alert(';(');
    });
}

function sendvalues_addlist(opc,namedoc,keyvalue,message){
     $.ajax({
        url: 'process.php',
        dataType: 'json',
        data: {"opc":opc, "namedoc":namedoc,"keyvalue":keyvalue,"message":message}
       
    }).done(function(data){   
        if(data != null){        
            if (data.error != '') {
               alert(data.error);
               return data;            }
        array = data.result;
        $('#editkeylist').find('option').remove();
        addOptions("editkeylist", array);
        }else{
           alert('no se obtuvo datos');
        }        
    }).fail(function(){
        alert(';(');
    });
}


/*load and copy file json  */
$(document).ready(function(){
    $('[data-toggle="popover"]').popover(); 
});

function baseName(str) {
    var base = new String(str).substring(str.lastIndexOf('/') + 1);
    if(base.lastIndexOf(".") != -1)       
        base = base.substring(0, base.lastIndexOf("."));
    return base;
}

//var filename = "";
$(document).ready(function(){
    $("#docinput").fileinput({
        allowedFileExtensions: ['json'],
        uploadUrl: "uploadfiles.php",
        maxFileSize: 10000000,
        showPreview: false,
        //dropZoneTitle: "",
        browseLabel: "",
        removeLabel: "",
        uploadLabel: ""
    }); 
});


                                                 /************all action button************/
/*Codigo a accion botón cargado json file*/
function myOnLoad(dirField){
    if (dirField.trim() != '') {
        dirField = document.getElementById("docinput").files[0].name; 
        if (true){
          sendvalues(1,dirField);  
        }
    }
    return true;
}

//$("#docinput").on("filebrowse", function(event) {
   // filename = "";
//});

$("#docinput").on("fileuploaded", function(event, data, previewId, index) {
    filename = data.response.name;
    filename = filename.replace(/ /g, "_");
    myOnLoad(dirField);    
});


$(document).ready(function() {
    $('#deletekey').click(function(e){
    dirField = document.getElementById("docinput").files[0].name; 
    kvalue = document.forms[0].editkeyvalue.value;
    deletScrit(dirField,kvalue);
    });
});

$(document).ready(function() {
    $('#saveaddtkey').click(function(e){
    createJson()
    });    
});

$(document).ready(function() {
    $('#saveedittem').click(function(event){
        var key_value = document.forms[0].editkeyvalue.value;
        var template = document.forms[0].edittemp.value;
        var doc_name = document.getElementById("docinput").files[0].name;
        var selectkeyval = $("#editkeylist").val();
        editjson(doc_name,key_value,selectkeyval,template);
    });   
});

$(document).ready(function() {
    $('#savefileedit').click(function(event){
        namedoc = document.getElementById("docinput").files[0].name;
        downloadfile(namedoc)
    });
});
                                                    /************end eyelash editar************/    
