
var meUserbox = {};
var youUserbox = {};
var timeMessage;
var message = "";
var sessionID = tokenGenerator();
youUserbox.avatar = "resources/images/bot_icon.png";
meUserbox.avatar = "resources/images/user_icon.png";
initialize(new Date());

function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+ minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}            

function tokenGenerator() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    s4() + '-' + s4() + s4() + s4();
}

function insertChat(who, text, time=0){
    var control = "";
    var date = formatAMPM(new Date());
    
    if (who == "me"){        
        control = '<li style="width:100%">' +
                        '<div class="msj macro">' +
                            '<div class="avatar">' + 
                                '<img class="img-circle" style="width:100%;" src="' + meUserbox.avatar + '" />' + 
                            '</div>' +
                            '<div class="text text-l">' +
                                '<p>' + text + '</p>' +
                                '<p><small>' + date + '</small></p>' +
                            '</div>' +
                        '</div>' +
                    '</li>';                    
    }else{
        control = '<li style="width:100%;">' +
                        '<div class="msj-rta macro">' +
                            '<div class="text text-r">' +
                                '<p>' + text + '</p>' +
                                '<p><small>' + date + '</small></p>' +
                            '</div>' +
                            '<div class="avatar" style="padding:0px 0px 0px 10px !important">' + 
                                '<img class="img-circle" style="width:100%;" src="' + youUserbox.avatar + '" />' +
                            '</div>' +
                        '</div>' +                                
                  '</li>';
    }
    setTimeout(function() {                        
            $("ul").append(control);
        }, time
     );    
}

function initialize(date){
    $("ul").empty();
    timeMessage = date.getTime();
    var hours = date.getHours();
    var greeting = hours >= 12 ? "Buenas tardes" : "Buenos dias";
    insertChat("you", greeting + ", bienvenido al chat de la Cámara de Comercio de Bogotá, ¿en qué le puedo colaborar?");
    $.ajax({
        url: "process.php",
        data: {"sessionID" : sessionID, "isSessionActive" : true, "message" : ""},
        dataType: "json"
    }).fail(function() {
        alert("Oops... an error occurred (1)");
    }); 
}

$(".textbox").on("keyup", function(e){
    if (e.which == 13){        
        var text = $(this).val();
        if (text != ""){
            message += text + " ";           
            insertChat("me", text);
            $(this).val('');

            var date = new Date();
            var time = date.getTime() - timeMessage;
            if (time > 0){
                $.ajax({
                    url: "process.php",
                    data: {"sessionID" : sessionID, "isSessionActive" : true, "message" : message},
                    dataType: "json"
                }).done(function(data) {        
                    if (data.error != "") {
                        alert(data.error);
                        return;
                    }
                    result = data.result;
                    if (result != "") {
                        result = result.split("[newmessage]")
                        for (i = 0; i < result.length; i++) {
                            insertChat("you", result[i]);
                        }
                    }

                }).fail(function() {
                    alert("Oops... an error occurred (2)");
                });
                message = "";
            }
            timeMessage = date.getTime();
        }       
    }
});

window.onbeforeunload = invalidarId;
function invalidarId () {
    if (true){
        $.ajax({
            url: "process.php",
            data: {"sessionID" : sessionID, "isSessionActive" : false, "message" : ""},
            dataType: "json"
        }).fail(function() {
            alert("Oops... an error occurred (3)");
        });
    }
}
