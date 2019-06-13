// const fs = require("fs"); // Or `import fs from "fs";` with ESM


setInterval(function()
{
    // path = new FileReader();
    // path.
    // if (fs.existsSync(path)) {
        

    // }
}, 2000); // poll every 2 seconds [is it too much? too little?]


$(document).ready(interval = setInterval(function()
{
    var source = $('#image_src').data().name;
    var image_name = $('#image_url').data().name; 
    if(image_name) {
        path = new Image();
        var url_image = source + image_name;
        path.src = url_image
        if (path.width != 0) {
            document.getElementById("overlay").style.display = "block";
            
        }
        else{
            document.getElementById("overlay").style.display = "none";
        }
    }   

}, 2000));

//$(document).onload(
//function () {
//    document.getElementById("overlay").style.display = "block";
// })

function off() {
clearInterval(interval); 
document.getElementById("overlay").style.display = "none";
}