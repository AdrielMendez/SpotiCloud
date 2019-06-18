console.log('from formOverlay js');

$('button#formOverlay').click(function(){
    console.log('button clicked');
  $.ajax({
      url: "/form",
      type: "POST",
      success: function(resp){
        console.log('inside forOverlay Success');
        document.getElementById("displayForm").style.display = "block";
        $('#displayForm').append(resp.form_data);

      }
  });
});

function off() {
    document.getElementById("formOverlay").style.display = "none";
}
