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
        if (numResults > 1) {
            $("#multiUsersFoundModal").show();
            for (var x = 0; x < numResults; x++) {
                $("#multiUsersFoundTable > tbody:last").append("<tr class=\"multiUserFoundResult\"><td>"+result[x].first_name+"</td><td>"+
                result[x].last_name+"</td><td>"+result[x].email+"</td></tr>");

                console.log(result[x]);
            }

            $(".multiUserFoundResult").click(function(event) {
                console.log($(event.target).parent());
                var firstName  = $(event.target).parent().children('td').eq(0).html();
                var lastName   = $(event.target).parent().children('td').eq(1).html();
                var email      = $(event.target).parent().children('td').eq(2).html();
                $("#customerFirstName").val(firstName);
                $("#customerLastName").val(lastName);
                $("#customerEmail").val(email);
                $("#multiUsersFoundModal").hide();
            });
        } else if (numResults == 1) {
            var firstName = result[0].first_name;
            var lastName = result[0].last_name;
            var email = result[0].email
            $("#customerFirstName").val(firstName);
            $("#customerLastName").val(lastName);
            $("#customerEmail").val(email);
            console.log(result);
        } else {
        }
    };

    $("#userNotFoundModalClose").click(function(event) {
        $("#userNotFoundModal").hide();
    });

    $("#newCustomerModalClose").click(function(event) {
        $("#newCustomerModal").hide();
    });

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
            }, function() {
                $("#userNotFoundModal").show();
            });
        // If no e-mail was entered, let's search by first and last name if they entered both
        } else if ($("#customerFirstName").val() && $("#customerLastName").val()) {
            User.findOne({FullName: $("#customerFirstName").val()+" "+$("#customerLastName").val()}, function(User) {
                populateInfo(User);
            }, function() {
                $("#userNotFoundModal").show();
            });
        // Finally, let's search by first name or last name if they only entered one
        } else if (($("#customerFirstName").val() || $("#customerLastName").val())) {
            if ($("#customerFirstName").val()) {
                oneName = $("#customerFirstName").val();
            } else if ($("#customerLastName")) {
                oneName = $("#customerLastName").val();
            }
            User.findOne({OneName: oneName}, function(User) {
                populateInfo(User);
            }, function() {
                $("#userNotFoundModal").show();
            });
        }
        $("#userNotFoundModalClose").click(function() {
            $("#userNotFoundModal").hide();
        });
    });

    $("#mainrow").on("click", "#newReservationNewCustomerBtn", function(event) {
        /**
         * This function handles adding a new customer to the system.
         */
        event.preventDefault();
        $("#newCustomerModal").show();
    });

    $("#mainrow").on("click", "#addNewActionBtn", function(event) {
        /**
         * This function handles adding a new action to a reservation.
         */
        event.preventDefault();
        steal.dev.log("Appending new action");
        var actionType = $("#actionType").val();
        var actionTypeName = $("#actionType option:selected").text();
        var actionOperator = $("#actionOperator").val();
        var actionStart = $("#startDateTime").data('date');
        var actionEnd = $("#endDateTime").data('date');
        var actionOrigin = $("#actionOrigin").val();
        var actionOriginName = $("#actionOrigin option:selected").text();
        var actionDestination = $("#actionDestination").val();
        var actionDestinationName = $("#actionDestination option:selected").text();

        $("#newReservationActions").append('<div id="individualAction" class="well reservationActionDiv" data-actiontype="'+actionType+'" data-origin="'+actionOrigin+'" data-destination="'+actionDestination+'" data-start="'+actionStart+'" data-end="'+actionEnd+'"><button type="button" class="btn btn-danger btn-xs pull-right del-action-btn"><span class="glyphicon glyphicon-remove"></span></button><div><font size=6>'+actionTypeName+'</font><br /><font size=2>Between '+actionStart+' and '+actionEnd+'</font><br /><font size=4>From '+actionOriginName+' to '+actionDestinationName+'<br />Equipment:</font><br /><ul id="equipmentList"><li>Item 1</li></ul></div>' +'<div class="equipmentAssignedToActionDiv"></div></div>');
    });

/*
* TODO: how to add form the client
* Create the reservation, getting its pk
*     for each action in $("#newReservationActions")
*         create the action, getting its pk
*         for each item attached
*             add item to action
*         add the action to the reservation
*/

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
        $("#newReservationActions").children("#individualAction").each( function () {
            steal.dev.log(jQuery.data($(this),"actiontype"));
        });
        $("#applyToAllActionsChkDiv").append('<br /><input type="checkbox" id="testActionBox" value="applyToTestAction" checked/>Test action')
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
            $("#newReservationEquipment").append('<div class="equipmentEntry well">#'+success.ItemID+' '+success.Description+'</div>');
            $('.reservationActionDiv .equipmentAssignedToActionDiv').each(function(index) {
                steal.dev.log('Appending equipment to Action');
                $(this).append('<div class="equipmentForAction" id="equipmentForAction-'+success.ItemID+'">#'+success.ItemID+' '+success.Description +
                    '<button type="button" class="removeEquipmentFromActionBtn btn btn-xs btn-danger pull-right">Remove</button>' +
                    '</div>');
            });

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