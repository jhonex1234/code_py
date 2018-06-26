                        /************************************Validation view Tree Editor************************************/

                                                 /************all validation ************/

//list check file
$(document).ready(function() {
    $("#exis_tree").attr('disabled', true);
    $("#exis_temfile").attr('disabled', true);
    $("#exis_ppklfile").attr('disabled', true);
    $("#id_state_create").attr('disabled', true);
});

//type file
function fileValidation(){
    var fileInput = document.getElementById('docinput');
    var filePath = fileInput.value;
    allowedExtensions = /(.json|.pkl)$/i;
    if(!allowedExtensions.exec(filePath)){
        alert('Archivo no valido unicamente .json/ .pkl ');
        document.getElementById("docinput").value = "";
        return false;
    }
    return false;
}


                                                 /************end validation************/
