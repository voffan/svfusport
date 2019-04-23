console.log("drunya");
$(document).ready(function(){
//    $('#team').click("click", function(){
//        alert("gfgjgjhgh");
//        $('#one').css('display', 'block');
//    })
//});

function getCookie(name) { //получить токен с сервера вроде
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


    $('#team').bind("change keyup input click", function(){
        if(this.value.length >= 2){
            $.ajax({
                type: 'POST',
                url: 'memberTeam/',
                data: {team: this.value,},
                success: function(data){

                    if(data.teams[0] == 'true'){

                        $('#falseTeam').css('display', 'block').hide(11000, function(){
                               $('#falseTeam').css('display', 'none');

                        })
                    }
                    else{
                        $('#trueTeam').css('display', 'block').hide(11000, function(){
                            $('#trueTeam').css('display', 'none');
                        })
                    }
                        //alert("gfgjgjhgh");
                }
            })

        }
    });


//    $(".search_result").hover(function(){
//        $('#team').blur();
//    })
//      ' + team.members.name + '
//    $(".search_result").on('click', 'li', function(){
//        s_user = $(this).text();
//        $(".search_result").fadeOut();
//    })
});