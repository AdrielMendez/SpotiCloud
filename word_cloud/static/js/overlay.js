
$('button#genBtn').click(function(){
    console.log('button clicked')
  $.ajax({
      url: "/cloud_task/",
      type: "POST",
      success: function(resp){
        console.log(resp.data);
        document.getElementById("overlay").style.display = "block";
        $('#overlay').append(resp.data);
      }
  });
});

function off() {
    document.getElementById("overlay").style.display = "none";
}