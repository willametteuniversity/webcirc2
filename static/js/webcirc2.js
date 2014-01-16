$(document).ready(function() {
    $("#registerBtn").on("click", function(event) {
       $("#mainrow").load("/registerNewUser/");
    });
});