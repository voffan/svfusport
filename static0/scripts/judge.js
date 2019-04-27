j=false;
$(".None").hide();
i = $("#id_form-TOTAL_FORMS").attr("value");
function showform(){
  if(j==false){
    $(".None").show();
    j=true;
  }
  else{
    var data = $("#forclone").clone().appendTo("#judge_div");
    data.find("label").eq(0).attr("for","id_form-" + i + "-judge");
    data.find("label").eq(1).attr("for","id_form-" + i + "-judge_position");
    data.find("label").eq(2).attr("for","id_form-" + i + "-DELETE");
    data.find("select").eq(0).attr("name","form-" + i + "-judge");
    data.find("select").eq(0).attr("id","id_form-" + i + "-judge");
    data.find("select").eq(1).attr("name","form-" + i + "-judge_position");
    data.find("select").eq(1).attr("id","id_form-" + i + "-judge_position");
    data.find("input").eq(1).attr("value","");
    data.find("input").eq(0).attr("name","form-" + i + "-DELETE");
    data.find("input").eq(1).attr("name","form-" + i + "-id");
    data.find("input").eq(0).attr("id","id_form-" + i + "-DELETE");
    data.find("input").eq(1).attr("id","id_form-" + i + "-id");
    i++;
    $("#id_form-TOTAL_FORMS").attr("value", i);
  }
}
