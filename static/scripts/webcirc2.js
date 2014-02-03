$(document).ready(function() {
    steal("can/can.js", function() {

    });
    steal("scripts/models/collection.js", function() {
    });
    steal("scripts/models/label.js", function() {
    });

    $("#registerBtn").on("click", function(event) {
        /**
         * This function handles the register button being clicked on the main page.
         */
       $("#mainrow").load("/registerNewUser/");
    });

    $("#signInBtn").on("click", function(event) {
        /**
         * This function handles a user wanting to sign in
         */
        event.preventDefault();
        var loginForm = $("#signInForm").serialize();
        $.post("/login/", loginForm, function(response){
            location.reload();
        });
    });

    $("#labelAndCategoryMgmtLink").on("click", function(event) {
        /**
         * This function handles the register button being clicked on the main page.
         */
       $("#mainrow").load("/labelAndCategoryMgmt/");
    });

    $("")
    $("#mainblock").on("click", "#submitRegistrationBtn", function(event) {
        /**
         * This function handles the submission of a new operator registration form.
         */
        var newOperatorForm = $("#registrationForm").serialize();
        $.post("/registerNewUser/", function(response) {
            $("#registrationFormBody").html(response);
        });
    });
});