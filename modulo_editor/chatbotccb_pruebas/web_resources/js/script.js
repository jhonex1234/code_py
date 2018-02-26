var timeMessage;
var message = '';
var sessionID = tokenGenerator();
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

function timeGreeting() {
    date = new Date()
    return date.getHours() >= 12 ? 'Buenas tardes' : 'Buenos dias';
}

function initialize(date){
    timeMessage = date.getTime();    
    sendMessage(timeGreeting() + ', bienvenido al chat de la Cámara de Comercio de Bogotá, ¿en qué le puedo colaborar?', 'left');
}

function inquire(text){
    if (text.trim() != '') {
        message += text + ' ';
        sendMessage(text, 'right');
        var date = new Date();
        var time = date.getTime() - timeMessage;
        if (time > 0){
            $.ajax({
                url: 'process.php',
                data: {'sessionID' : sessionID, 'isSessionActive' : true, 'message' : message},
                dataType: 'json'
            }).done(function(data) {
                if (data.error != '') {
                    alert('error')
                    alert(data.error);
                    return;
                }
                result = data.result;
                result = result.replace('[UserName]', 'Juan Carlos');
                result = result.replace('[TimeGreeting]', timeGreeting());
                if (result != '') {
                    result = result.split('[NewMessage]');
                    for (i = 0; i < result.length; i++)
                        sendMessage(result[i], 'left', 300);
                }

            }).fail(function() {
                alert('Oops... an error occurred (2)');
            });
            message = '';
        }
        timeMessage = date.getTime();
    }
}

function sendMessage(text, side, time=0) {
    $('.message_input').val('');
    var $message = $($('.message_template').clone().html());
    $message.addClass(side).find('.text').html(text);
    $message.find('.date').html(formatAMPM(new Date()));
    $('.messages').append($message);
    setTimeout(function () {
        $message.addClass('appeared');
    }, time);
    return $('.messages').animate({scrollTop: $('.messages').prop('scrollHeight')}, 300);
}

$('.send_message').click(function (e) {
    return inquire( );
});

$('.message_input').keydown(function (e) {
    if (e.which === 13) {
        return inquire($('.message_input').val());
    }
});

window.onbeforeunload = invalidarId;
function invalidarId () {
    if (true){
        $.ajax({
            url: 'process.php',
            data: {'sessionID' : sessionID, 'isSessionActive' : false, 'message' : ''},
            dataType: 'json'
        }).fail(function() {
            alert('Oops... an error occurred (3)');
        });
    }
}
