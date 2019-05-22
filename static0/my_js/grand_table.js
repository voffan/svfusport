console.log("dryyynya");

$(document).ready(function(){

$('#button').bind("click", function(){
//    function viewTable(){
//        var data = [
//            {begin: $('input[name=begin]').val()},
//            {end: $('input[name=end]').val()}
//
//        ];
//        var da = $('input').serialize()
        $.ajax({
                type: 'POST',
                url: 'grand_t/',
                data: {begin: $('input[name=begin]').val()},
                success: function(data){
                    var $body = $('#table').find('tbody');
                    $body.html('');
                    $.each(data.teams, function(ind, team) {
                        $body.append('<tr><td></td><td>' + team.name + '</td><td>' + team.members + '</td><td></td><td></td></tr>');
                    });
                }
            });
//    }
});

});