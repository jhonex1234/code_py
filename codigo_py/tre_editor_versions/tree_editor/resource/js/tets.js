function senditemjson(opc,namedoc,model,state,filesuport,val,modval,final_state,initial_state,max_attempts  ){
$.ajax({
        url: 'process.php',
        dataType: 'json',
        data: {'opc':opc,'namedoc':namedoc, ,"filesuport":filesuport, 'is_forboo':is_forboo,'final_state':final_state,
  'model':model,'topic':topic,'label':label,'state':state,'initial_state':initial_state,
  'final_state':final_state ,'max_attempts':max_attempts}
       
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
              
              array.sort();
              array_2.sort();
              array_3.sort();
              array_4.sort();
              
              $('#lis_models_make_model').find('option').remove();
              addOptions('lis_models_make_model', array_2);
              
              
              $('#topic_list').find('option').remove(); 
              addOptions('topic_list', array_4);

              $('#lis_models_make_label').find('option').remove();
              addOptions('lis_models_make_label', array_2);
              
              
              $('#lis_label_make_label').find('option').remove();
              addOptions('lis_label_make_label', array_3);

              $('#lis_label_make_trans').find('option').remove();
              addOptions('lis_label_make_trans', array_3);

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
function makemodel(namedoc,model,state){
  senditemjson(61,namedoc,model,state)
}