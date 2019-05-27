j=false;
$(".None").hide();
i = $("#id_form-TOTAL_FORMS").attr("value");
function showsportsmanform(){
  if(j==false){
    $(".None").show();
    j=true;
  }
  else{
    var data = $("#forclone").clone().appendTo("#sportsman_div");
    data.find("label").eq(0).attr("for","id_form-" + i + "-sportsman");
    data.find("label").eq(1).attr("for","id_form-" + i + "-comments");
    data.find("label").eq(2).attr("for","id_form-" + i + "-DELETE");
    data.find("select").eq(0).attr("name","form-" + i + "-sportsman");
    data.find("select").eq(0).attr("id","id_form-" + i + "-sportsman");
    data.find("select").eq(1).attr("name","form-" + i + "-comments");
    data.find("select").eq(1).attr("id","id_form-" + i + "-comments");
    data.find("input").eq(1).attr("value","");
    data.find("input").eq(0).attr("name","form-" + i + "-DELETE");
    data.find("input").eq(1).attr("name","form-" + i + "-id");
    data.find("input").eq(0).attr("id","id_form-" + i + "-DELETE");
    data.find("input").eq(1).attr("id","id_form-" + i + "-id");
    i++;
    $("#id_form-TOTAL_FORMS").attr("value", i);
  }
}
