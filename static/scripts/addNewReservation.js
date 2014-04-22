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
    });

    $("#mainrow").on("click", "#showAddEquipmentModalBtn", function(event) {
        /**
         * This button handles displaying the modal window to add new equipment to
         * a reservation
         */
        steal.dev.log("Bringing up add equipment modal");
        $("#addEquipmentModal").modal('show');
    });

    $("#mainrow").on("click", "#addEquipmentBtn", function(event) {
        /**
         * This button handles searching the server for an inventory item and adding it to
         * a reservation.
         */
        var invItemId = $("#equipmentId").val();

        steal.dev.log("Searching for equipment ID: "+invItemId);
        InventoryItem.findOne({id: invItemId}, function(success) {
            steal.dev.log("Found an item");
            console.log(success);
            $("#newReservationEquipment").append('<div class="equipmentEntry well">#'+success.ItemID+' '+success.Description+'' +
                '</div>')
            $("#addEquipmentModal").modal('hide');
        }, function(error) {
            $(".alert-equipment-not-found").hide();
            $("#addEquipmentModalBody").prepend('<div class="alert alert-danger alert-dismissable alert-equipment-not-found">' +
                '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
                '<strong>Error!</strong> An item with that ID was not found! Please try again.' +
                '</div>');
        });
    });
})