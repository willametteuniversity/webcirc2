steal(function() {
    var populateInfo = function(result) {
        /**
         * This function handles populating the information into the form from a
         * retrieved customer.
         * @type {number}
         */
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
        /**
         * This function handles trying to find a customer based on what they entered into
         * the form.
         */
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
        /**
         * This function handles adding a new customer to the system.
         */
        event.preventDefault();
        steal.dev.log("New Customer Btn clicked!");
    });

    $("#mainrow").on("click", "#addNewActionBtn", function(event) {
        /**
         * This function handles adding a new action to a reservation.
         */
        event.preventDefault();
        steal.dev.log("Appending new action");
        var actionType = $("#actionType").val();
        var actionOperator = $("#actionOperator").val();
        var actionStart = $("#startDateTime").data('date');
        var actionEnd = $("#endDateTime").data('date');
        var actionOrigin = $("#actionOrigin").val();
        var actionDestination = $("#actionDestination").val();
        $("#newReservationActions").append('<div class="well"><button type="button" class="btn btn-danger btn-xs pull-right del-action-btn"><span class="glyphicon glyphicon-remove"></span></button><div>'+actionType+' by '+actionOperator+' from '+actionStart+' to '+actionEnd
                                            +' origin '+actionOrigin+' to '+actionDestination+'</div></div>');

    });

    $("#mainrow").on("click", ".del-action-btn", function(event) {
        /**
         * This function handles deleting an action from a reservation.
         */
        steal.dev.log("Deleting an action");
        $(this).parent().remove();
    })
})