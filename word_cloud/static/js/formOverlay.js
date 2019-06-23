console.log('from formOverlay js');

var formOverlay = document.getElementById('displayFormOverlay');
var formframe = document.getElementById('form_frame');

$('button#formOverlay').click(function(){
    console.log('button clicked');
  $.ajax({
      url: "/form",
      type: "POST",
      success: function(resp){
        console.log('inside forOverlay Success');
        document.getElementById("displayFormOverlay").style.display = "block";
        $('#displayFormOverlay').append(resp.form_data);
      }
  });
});


// this is not currently working
$('button#custBtn').click(function() {
    console.log('create custom button was clicked!!!!!!')
    formOff();

});



function formOff() {
    console.log("turned form off!")
    document.getElementById("displayFormOverlay").style.display = "none";
    document.getElementById("displayFormOverlay").innerHTML = '';


}

// $('button#genBtn').click(function(){
    //     console.log('button clicked')
    //   $.ajax({
    //       url: "/cloud_task/",
    //       type: "POST",
    //       success: function(resp){
    //         console.log(resp.data);
    //         document.getElementById("overlay").innerHTML = "<h1>IN THE CLOUD_TASK AJAX CALL!!!!!~!~!~!~!~!~</h1>";
    //         document.getElementById("overlay").style.display = "block";
    //         $('#overlay').append(resp.data);
    //       }
    //   });
    // });

