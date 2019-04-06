console.log("work");
$(document).ready(function(){



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
        if(this.value.length >=2){
            $.ajax({
                type: 'POST',
                url: 'memberTeam/',
                data: {team: this.value,},
                success: function(data){
                    var $body = $('#table').find('tbody');
                    $body.html('');
                    $.each(data.teams, function(ind, team) {

                        $.each(team.members, function(ind2, mem){

                            $body.append('<tr><td></td><td>' + team.name + '</td><td>' + mem.name + '</td><td>' + mem.comm + '</td><td>'+
                                '<div class="dropdown">'+
                                    '<a class="btn btn-light dropdown-toggle-none" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Операции</a>'+
                                    '<div class="dropdown-menu" aria-labelledby="dropdownMenuLink">'+

                                    '<a class="dropdown-item" href="/CM/membercreate/">Добавить спортсмена</a>' +
                                    '<a class="dropdown-item" href="/CM/tmembertable/'+mem.id+'/membChange/"">Редактировать спортсмена</a>'+
                                    '<a class="dropdown-item" href="/CM/tmembertable/'+mem.id+'/membremove/"">Удалить спортсмена</a>'+

                                    '</div>'+
                                '</div>'+

                                '</td></tr>');

                        })

                    });
                }
            });
        };

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