steal(function() {
    var populateInfo = function(result) {
        var numResults = 0;
        $.each(result, function(key) {
            if ($.isNumeric(key)) {
                numResults += 1;
            }
        });
        if (numResults > 0) {
            for (var x = 0; x < numResults; x++) {
                console.log(result[x]);
            }
        } else {
            console.log(result);
        }
    };
    $("#mainrow").on("click", "#newReservationFindCustomerBtn", function(event) {
        event.preventDefault();
        // Let's search by their e-mail first

        if ($("#customerEmail").val()) {
            User.findOne({id: $("#customerEmail").val()}, function(User) {
                populateInfo(User);
            });
        } else if ($("#customerFirstName").val() && $("#customerLastName").val()) {
            User.findOne({FullName: $("#customerFirstName").val()+" "+$("#customerLastName").val()}, function(User) {
                populateInfo(User);
            });
        } else if (($("#customerFirstName").val() || $("#customerLastName").val())) {
            if ($("#customerFirstName").val()) {
                oneName = $("#customerFirstName").val();
            } else if ($("#customerLastName")) {
                oneName = $("#customerLastName").val();
            }
            User.findOne({OneName: oneName}, function(User) {
                populateInfo(User);
            });
        }


    });

    $("#mainrow").on("click", "#newReservationNewCustomerBtn", function(event) {
        event.preventDefault();
        steal.dev.log("New Customer Btn clicked!");
    });

    $("#mainrow").on("click", "#addNewActionBtn", function(event) {
        event.preventDefault();
        var existingActions = $(".reservationAction");
        if (existingActions.length == 0) {
            var startingPoint = $("#newReservationsActionsHelp").append()
        }
    });

    var constructNewAction = function() {
        
    }
})