$(document).ready(function() {
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    steal("can/can.js", function() {});
    steal("scripts/utility.js", function() {});
    steal("scripts/models/collection.js", function() {});
    steal("scripts/models/label.js", function() {});
    steal("scripts/labelAndCategoryMgmt.js", function() {
        $.ajaxPrefilter(function(options, originalOptions, jqXHR) {
            /**
             * This function handles inserting out CSRF token into outgoing
             * AJAX requests
             */
            if ( options.processData
            && /^application\/json((\+|;).+)?$/i.test( options.contentType )
            && /^(post|put|delete)$/i.test( options.type )
            ) {
                options.data = JSON.stringify( originalOptions.data );
            }
            if (!options.crossDomain) {
                if (csrftoken) {
                    return jqXHR.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });




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
         $("#mainrow").load("/labelAndCategoryMgmt/", function() {
             loadLabels();
         });

    });

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