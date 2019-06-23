function customDimension(that) {
    // console.log(that.value)
    if (that.value == "custom") {
        document.getElementById("customDimensions").style.display = "block";
    } else {
        document.getElementById("customDimensions").style.display = "none";
    }
}