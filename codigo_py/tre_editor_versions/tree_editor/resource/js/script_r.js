                        /************************************Edition resource tree************************************/
                        /************all action button************/
//create state
$(document).ready(function(){
    $('#add_clave_tree_state').click(function(event){
         namedoc = document.forms[0].file_tree_load_suport.value;
         va_l = document.forms[0].state_id.value;
        insertState(namedoc,va_l);
        document.forms[0].filetreeload.value = '';

    });
     return false;
});

//edit state
$(document).ready(function(){
    $('#edit_clave_tree_state').click(function(event){
      combo = document.getElementById("lltemplates_selec");
      namedoc = document.forms[0].file_tree_load_suport.value;   
      va_l = document.forms[0].state_id.value;
      mod = combo.options[combo.selectedIndex].text;
      document.forms[0].filetreeload.value = '';
      editState(namedoc,va_l,mod);
    });
     return false;
});

// list selection
function scheduleA(event) {
    if(this.options[this.selectedIndex].value == 1){
       namedoc = document.forms[0].filetreeload.value;
       dirField =  document.forms[0].file_tree_load_suport.value;
       document.forms[0].file_tree_pkl_suport.value = namedoc;
       namefilemodel = document.forms[0].file_tree_pkl_suport.value;
       load_keys_trai(dirField,namedoc,namefilemodel);
    }
    if(this.options[this.selectedIndex].value == 2){
       namedoc = document.forms[0].filetreeload.value;
       dirField =  document.forms[0].file_tree_load_suport.value;

       load_template_key(dirField,namedoc);
       $('#llstate_selec').find('option').remove();
    }
    if(this.options[this.selectedIndex].value == 3){
       $("#newfield_r").attr('disabled', true);
       $('#llstate_selec').find('option').remove();
       name =  document.forms[0].filetreeload.value;
       document.forms[0].file_tree_load_suport.value = name;
       document.forms[0].filetreeload.value = '';
       namedoc = document.forms[0].file_tree_load_suport.value;

       loadConfigFileTree(namedoc);
    }
    if(this.options[this.selectedIndex].value == 4){
       $("#newfield_r").attr('disabled', false);
       $("#newfield_r").attr('checked', true);
       createField(true);

    }
}
                                                 /************end action button************/

                                             /************all function ctr************/

function loadConfigFileTree(namedoc){
   
  alert('recuerde cargar los recursos, para la edicion de este archivo de configuracion');
    $("#exis_tree").attr('disabled', false);
    $("#exis_tree").attr('checked', true);
    $("#exis_tree").attr('disabled', true);

  $("#resouceSelec option[value=4]").remove();
  sendName_Model(5,namedoc,namedoc,'','','','df','df',1,'')
   
}

function createField(value){
    namedoc = document.forms[0].filetreeload.value;
    if(value == true){
        makenewfile(namedoc); 
    }
}

//create file
function makenewfile(namedoc){
    if (namedoc.length != ''){
      sendFile(1,namedoc,namedoc,'','','','df','df',1,'');
      $("#resouceSelec option[value=4]").remove();
      $("#newfield_r").attr('disabled', true);
      $("#exis_tree").attr('disabled', false);
      
      $("#exis_tree").attr('checked', true);
      $("#exis_tree").attr('disabled', true);
        
        return false;

     }else{
      
      alert('!No se pudo completar accion, campo documento no diligenciado¡');
      $("#newfield_r").attr('checked', false);
      $("#newfield_r").attr('disabled', false);
      $("#exis_tree").attr('checked', false);
      
      return false;      
    }
}


//ctr load template file
function load_template_key(filesuport,dirField){
    if (filesuport.trim() != '') {
        if (dirField.trim() != ''){
          sendFile(3,filesuport,dirField,'','','','df','df',1,''); 
          //exis_temfile
      $("#resouceSelec option[value=2]").remove();
      $("#exis_temfile").attr('checked', true);
      $("#exis_temfile").attr('disabled', true);
      document.forms[0].filetreeload.value = '';
        }else{
           document.forms[0].resouceSelec.value='0';
           alert('No se pudo completar la accion, el archivo no esta cargado');
        }
    }else{
      document.forms[0].resouceSelec.value='0';
        alert('No se pudo completar la accion, debe Crear o cargar un documento de tipo json para que este achivo sea asignado');
    }
    return false;
}

function load_keys_trai(filesuport,dirField,namefilemodel){
  allowedExtensions = /(.pkl)$/i;
  if (filesuport.trim() != ''){
      if (dirField.trim() != ''){
          if(!allowedExtensions.exec(namefilemodel)){
            alert('El archivo cargado no tiene el formato plk, debe cargar   un archivo con formato pkl');
            document.forms[0].resouceSelec.value='0';
            document.forms[0].filetreeload.value = '';
            return false;
          }else{
            sendFile(4,filesuport,dirField,namefilemodel,'','','df','df',1,'');
            $("#resouceSelec option[value=1]").remove();
            $("#exis_ppklfile").attr('checked', true);
            $("#exis_ppklfile").attr('disabled', true);
            document.forms[0].filetreeload.value = '';
            document.forms[0].resouceSelec.value='0';
            return false;
          } 
        }else{
           document.forms[0].resouceSelec.value='0';
           alert('No se pudo completar la accion, el archivo no esta cargado');
        }
    }else{
      document.forms[0].resouceSelec.value='0';
        alert('No se pudo completar la accion, debe Crear o cargar un documento de tipo json para que este achivo sea asignado');
    }
    return false;      
  
}
//ctr create state
function insertState(namedoc,va_l){
    if(namedoc.length != ''){
        if(va_l.length != ''){
          $('#llstate_selec').find('option').remove();
          
 
          sendFile(2,namedoc,'','',va_l,'','df','df',1,'');
          $("#id_state_create").attr('checked', true);
          $("#id_state_create").attr('disabled', true);
          document.forms[0].state_id.value = '';
          document.forms[0].filetreeload.value = '';
         
        }else{
            alert('No se pudo completar la accion, campo nombre estado no debe ser nulo');
        }
    }else{
        alert('No se pudo completar la accion, campo nombre documento no debe ser nulo');

    }
}
function editState(namedoc,va_l,va_lmod){
 if(namedoc.length != ''){
        if(va_l.length != ''){
          sendFile(6,namedoc,namedoc,'',va_l,va_lmod,'df','df',1,'');
          $("#id_state_create").attr('checked', true);
          $("#id_state_create").attr('disabled', true);
          document.forms[0].state_id.value = '';
          document.forms[0].filetreeload.value = '';
        }else{
            alert('No se pudo completar la accion, campo nombre estado no debe ser nulo');
        }
    }else{
        alert('No se pudo completar la accion, campo nombre documento no debe ser nulo');

    } 
}

//add element to select (label) 
function addOptions(domElement, array) {
 var select = document.getElementsByName(domElement)[0];
 for (value in array) {
      var option = document.createElement("option");
      option.text = array[value];
      select.add(option);
      document.forms[0].filetreeload.value = '';
 }
}

      
function loadkey(value_1){
  msjwait = ['Cargando']
  $('#lis_label_make_trans').find('option').remove();
  addOptions('lis_label_make_trans', msjwait);

  namedoc = document.forms[0].file_tree_load_suport.value;
  filesuport = document.forms[0].file_tree_load_suport.value;
  namefilemodel = document.forms[0].file_tree_pkl_suport.value; 
  sendNameModel(01,namedoc,filesuport,namefilemodel,'','','','','',value_1);

}

function sendStateSelect_init(value_1){
  document.forms[0].est_init.value= value_1;
}

function sendStateSelect_end(value_1){
   document.forms[0].est_end.value= value_1;

}




function loadkey_2(value_1){
  msjwait = ['Cargando']
  $('#label_model_2').find('option').remove();
  addOptions('label_model_2', msjwait);

  namedoc = document.forms[0].file_tree_load_suport.value;
  filesuport = document.forms[0].file_tree_load_suport.value;
  namefilemodel = document.forms[0].file_tree_pkl_suport.value; 
  sendNameModel(01,namedoc,filesuport,namefilemodel,'','','','','',value_1);
} 

function insertimage(thisImg) {
    var img = document.createElement("img");
    img.src = '/demo/tree_editor/img/'+thisImg;
    document.getElementById('#igm_model').appendChild(img);
}

                                                /************End all function ctr************/

                                                  /************all function send************/
//tbl_topic


function loadtblmodel(data){
 var tblmodel = '<thead> '+'<tr>'+'<th>Modelos</th>'+
 '<th>Estado</th>'+'</tr>'+'</thead>'

 tblmodel+='<tbody>'
 for (var i = 1; i < data.length; i++) {
     tblmodel+= '<tr>'+
     '<td>'+data[i].id+'</td>'+'<td>'+data[i].state+'</td>'+
     '</tr>';
 }
 tblmodel+='</tbody>'
 $("#tbl_statemodel").append(tblmodel);
}

function loadtbltransitions(data){
 var tblmodel = '<thead> '+'<tr>'+'<th>Estado Inicial</th>'+
 '<th>Forzado</th>'+
 '<th>Etiqueta</th>'+
 '<th>Estado Final</th>'+
 '</tr>'+'</thead>'

 tblmodel+='<tbody>'
 for (var i = 1; i < data.length; i++) {
     tblmodel+= '<tr>'+
     '<td>'+data[i].starting_state+'</td>'+
     '<td>'+data[i].is_forced+'</td>'+
     '<td>'+data[i].label+'</td>'+
     '<td>'+data[i].ending_state+'</td>'+
     '</tr>';
 }
 tblmodel+='</tbody>'
 $("#tbl_data_trasitions").append(tblmodel);
}

function loadtbltemplate(data){
 var tblmodel = '<thead> '+
   '<th>Id Modelos</th>'+'<th>Plantilla</th>'+'<th>Estado</th>'+ 
    '<th>Tema</th>'+
  '</tr>'+'</thead>'

 tblmodel+='<tbody>'
 for (var i = 1; i < data.length; i++) {
     tblmodel+= '<tr>'+
     '<td>'+data[i].id+'</td>'+
     '<td>'+data[i].label+'</td>'+
     '<td>'+data[i].state+'</td>'+
     '<td>'+data[i].topic+'</td>'+
     '</tr>';
 }
 tblmodel+='</tbody>'
 $("#tbl_data_temp").append(tblmodel);
}

function sendName_Model(opc,namedoc,filesuport,namefilemodel,val,modval,final_state,initial_state,max_attempts,modelselect){
   $.ajax({
        url: 'process.php',
        dataType: 'json',
        data: {"opc":opc,"namedoc":namedoc, "filesuport":filesuport,"namefilemodel":namefilemodel,"val":val,"modval":modval,"final_state":final_state,  "initial_state":initial_state,"max_attempts":max_attempts,"modelselect":modelselect}
       
    }).done(function(data){   
        if(data != null){        
            if (data.error != ''){
               alert(data.error);
               return data;
            }
            selec = data.response_getid;
            if(selec == 1){
              
              data_models = data.response_getmodels;
              data_trasitions = data.response_gettransitions;
              data_template = data.response_gettemplates;
              img ='http://192.168.74.150/demo/tree_editor/img/'
              img += data.nameView; 
              document.getElementById('igm_model').src = img;
              //insertimage();  
              loadtblmodel(data_models);
              loadtbltransitions(data_trasitions);
              loadtbltemplate(data_template );
              var data_topic =  data.response_gettopics;

              //est_init
              document.forms[0].est_init.value = data.response_getstateinit;
              document.forms[0].est_end.value = data.response_getfinal_state;
              document.forms[0].try_max.value = data.response_getmax_attempts;

              document.forms[0].list_topic_normal.value = data_topic.normal;
              document.forms[0].list_topic_none.value = data_topic.none;
              alert('Archivo de configuracion cargado, exitosamente')
            }
        }else{
          alert('No se obtuvo datos, verifique La conexion');
        }
         
   });
}
function send_Name_Model(opc,namedoc,filesuport,namefilemodel,val,modval,final_state,initial_state,max_attempts,modelselect){
   $.ajax({
        url: 'process.php',
        dataType: 'json',
        data: {"opc":opc,"namedoc":namedoc, "filesuport":filesuport,"namefilemodel":namefilemodel,"val":val,"modval":modval,"final_state":final_state,  "initial_state":initial_state,"max_attempts":max_attempts,"modelselect":modelselect}
       
    }).done(function(data){   
        if(data != null){        
            if (data.error != '') {
               alert(data.error);
               return data;
            }

              array_5 = data.getlabelmodel;
              alert(array_5);
              $('#label_model_2').find('option').remove();
              addOptions('label_model_2', array_5);

        }else{
          alert('No se obtuvo datos, verifique La conexion');
        }    
   });
}

function sendNameModel(opc,namedoc,filesuport,namefilemodel,val,modval,final_state,initial_state,max_attempts,modelselect){
   $.ajax({
        url: 'process.php',
        dataType: 'json',
        data: {"opc":opc,"namedoc":namedoc, "filesuport":filesuport,"namefilemodel":namefilemodel,"val":val,"modval":modval,"final_state":final_state,  "initial_state":initial_state,"max_attempts":max_attempts,"modelselect":modelselect}
       
    }).done(function(data){   
        if(data != null){        
            if (data.error != '') {
               alert(data.error);
               return data;
            }
            if(data.getlabelmodel){
              array_5 = data.getlabelmodel;
              $('#lis_label_make_trans').find('option').remove();
              addOptions('lis_label_make_trans', array_5);
            }
               
        }else{
          alert('No se obtuvo datos, verifique La conexion');
        }    
   });
}

function sendFile(opc,namedoc,filesuport,namefilemodel,val,modval,final_state,initial_state,max_attempts,modelselect){
     $.ajax({
        url: 'process.php',
        dataType: 'json',
        data: {"opc":opc,"namedoc":namedoc, "filesuport":filesuport,"namefilemodel":namefilemodel,"val":val,"modval":modval,"final_state":final_state,  "initial_state":initial_state,"max_attempts":max_attempts,"modelselect":modelselect}
       
    }).done(function(data){   
        if(data != null){        
            if (data.error != '') {
               alert(data.error);
               return data;
           }

           var savename = document.forms[0].file_tree_load_suport.value; 
           if(savename == ''){ 
            document.forms[0].file_tree_load_suport.value = data.doc_name;
           }
           document.forms[0].filetreeload.value = '';

           if(data.result != []){

              array = data.result;
              array_2 = data.pkl_list;
              array_3 = data.template_list;
              array_4 =  data.topic_list; 
              array_5 = data.getlabelmodel;

              array.sort();
              array_2.sort();
              array_3.sort();
              array_4.sort();
              array_5.sort();

              $('#lis_models_make_model').find('option').remove();
              addOptions('lis_models_make_model', array_2);
              
              $('#topic_none').find('option').remove();
              addOptions('topic_none', array);
              
              $('#topic_normal').find('option').remove();
              addOptions('topic_normal', array);
              

              //
              //
              $('#lis_label_model_model_trans').find('option').remove();
              addOptions('lis_label_model_model_trans', array_2);
              

              $('#topic_list').find('option').remove(); 
              addOptions('topic_list', array_4);

              $('#lis_models_make_label').find('option').remove();
              addOptions('lis_models_make_label', array_2);
              
              
              $('#lis_label_make_label').find('option').remove();
              addOptions('lis_label_make_label', array_3);

              $('#lis_label_make_trans').find('option').remove();
              addOptions('lis_label_make_trans', array_5);

              $('#state_init_selec').find('option').remove();
              addOptions('state_init_selec', array);
              
              $('#state_end_selec').find('option').remove();
              addOptions('state_end_selec', array);
            

              $('#state_model').find('option').remove();
              addOptions('state_model', array);
              
              $('#state_label').find('option').remove();
              addOptions('state_label', array);

              $('#state_trans').find('option').remove();
              addOptions('state_trans', array);

              
              $('#lltemplates_selec').find('option').remove();
              addOptions('lltemplates_selec', array);
              

              $('#state_trans_ed').find('option').remove();
              addOptions('state_trans_ed', array);
             

              document.forms[0].filetreeload.value = '';
            }
           
           alert(data.msj);
        }else{
           alert('no se obtuvo datos');
        }        
    }).fail(function(){
        alert(';(');
    });
} 

// Copy File to Server
// load file type pkl
$(document).ready(function() {
    $('#upload').on('click', function() {
       file_data = $('#docinput').prop('files')[0];   
      if(file_data){    
          form_data = new FormData();                  
          form_data.append('file', file_data);
          $.ajax({
              url: 'upload.php',  
              dataType: 'text',  
              cache: false,
              contentType: false,
              processData: false,
              data: form_data,                         
              type: 'post',
              success: function(data){
                  document.forms[0].filetreeload.value = data;
                alert('Archivo cargado Exitosamete \n A la Espera Accion..');
             }
           });
      }else{
        alert(' \t\t\t\t\t\t\t\t\t\t\t\t \t\t\t\t\t\t\t\t\t\t \t\t\t\t\t\t\t\t\t\t\t\t Accion no completada \t \n \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t Archivo no Cargado \t ');
      }
        return false;
    });
});