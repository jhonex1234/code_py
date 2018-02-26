/*delete with keyvalue*/
function deletScrit(opc,keyvalue){
    if (keyvalue.trim() != '') {
        dirField = document.forms[0].docinput.value;
        template = document.forms[0].message.value;
        //1
        return true;
    }
}
/*send  key to input id="keyvalue" and
load template with keyvalue*/

function loadkey(keyvalue){
    document.forms[0].keyvalue.value=keyvalue;
    dirfield = document.forms[0].newnamefile.value;
    sendvalueskeys(3,dirfield,keyvalue);
    return true;
}

/*create new list templates */
function saveNewteplate(keyvalue,newtemplate){
    if(keyvalue.trim() != '' && newtemplate.trim() != ''){
        dirField = document.forms[0].docinput.value;
        //4
    }
    return true;
}

function editjson(keyvalue,editemplate){
    if(keyvalue.trim() != '' && editemplate.trim() != ''){
        dirField = document.forms[0].docinput.value;
        //6
    }
}

/*create new json file*/
function createJson(){
        dirField = document.forms[0].docinput.value;
        keyvalue = document.forms[0].keyvalue.value; 
        template = document.forms[0].message.value; 
       //5 
    return true;
}

function cleanField(namedoc){
    if (namedoc.trim() != '') {
        keyvalue = document.forms[0].keyvalue.value; 
        template = document.forms[0].message.value;
        createtemplatefile(7,namedoc); 
    } else {
        alert('no se a almacenado el nombre');
    }
 }

                                        /*action bottons*/
$(document).ready(function() {
    $('#almacenarjson').click(function(e){
    key_value = document.forms[0].keyvalue.value;
    template = document.forms[0].message.value;
    });    
});

$(document).ready(function() {
    $('#eliminarjson').click(function(e){
    key_value = document.forms[0].keyvalue.value;
    deletScrit(2,key_value);
    });
});

$(document).ready(function() {
    $('#makejsonfile').click(function(event){
        createJson();
    });
});
$(document).ready(function() {
    $('#editjson').click(function(event){
        key_value = document.forms[0].keyvalue.value;
        template = document.forms[0].message.value;
        editjson(key_value,template);
    });   
});
$(document).ready(function(){
    $('#nuevojson').click(function(event) {
        namedoc = $('#newnamefile').val();
        document.forms[0].keyvalue.value = '';
        document.forms[0].message.value = '';
        $('select').empty();
        cleanField(namedoc);
    });
});

/*Codigo a accion botón cargado json file*/
function myOnLoad(dirField){
    if (dirField.trim() != '') {
        if (true){
          sendvalues(1,'templates.json');  
        }
    }
    return true;
}

function createtemplatefile(opc,namedoc){
    $.ajax({
        url: 'process.php',
        dataType:'json',
        data:{'opc':opc,'namedoc':namedoc}
    }).done(function(data){
        
    }).fail(function(){
        alert(';(');
    });

}

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
            document.forms[0].message.value = data.msj;
          
        }else{
            error = 'no se obtuvo datos';
            document.forms[0].message.value = error;
            return true;
        }
    }).fail(function() {
        alert(';( error (1)');
    });
}
/*
params '{"opc":1,"namedoc":"template.json","keyvalue":'saludo,"template":'buenos dias',"newtemplate":"aun no","localitation":"template.json"}'
*/
function sendvalues(opc,namedoc){
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
        document.forms[0].newnamefile.value = data.doc_name;
        addOptions("keyvalueselect", array);
        }else{
            alert('no se obtuvo datos');
        }
    }).fail(function() {
        alert(';( error (1)');
    });
}
/*
return load select, load input template
*/



// Rutina para agregar opciones a un <select>
function addOptions(domElement, array) {
 var select = document.getElementsByName(domElement)[0];
 for (value in array) {
  var option = document.createElement("option");
  option.text = array[value];
  select.add(option);
 }
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

var filename = "";
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

$("#docinput").on("filebrowse", function(event) {
    filename = "";
});

$("#docinput").on("fileuploaded", function(event, data, previewId, index) {
    filename = data.response.name;
    filename = filename.replace(/ /g, "_");
});


