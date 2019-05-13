$(document).ready(function() {
$(".all").on("change", function() {
    var groupId = $(this).data('id');
    $('.one[data-id="' + groupId + '"]').prop("checked", this.checked);
  });
$(".one").on("change", function() {
    var groupId = $(this).data('id');
    var allChecked = $('.one[data-id="' + groupId + '"]:not(:checked)').length == 0;
    $('.all[data-id="' + groupId + '"]').prop("checked", allChecked);
    $('.all[data-id="' + groupId + '"]').prop("checked")
  });
});
function checkchekboxes(button) {
  submit = button.name;
  var data = [];
  $('.one:checkbox:checked').each(function() {
    data.push($(this).attr("id"));
  });
  console.log(data);
  $.ajax({
    url: "{% url 'sport:competition' %}",
    data: {
      'datajson': JSON.stringify(data),
      'operation': submit,
      'csrfmiddlewaretoken': '{{ csrf_token }}'
    },
    method: "POST",
  })
}
