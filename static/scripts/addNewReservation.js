steal(function () {
    var populateInfo = function (result) {
        /**
         * This function handles populating the information into the form from a
         * retrieved customer.
         * @type {number}
         */
        var numResults = 0;
        $.each(result, function (key) {
            if ($.isNumeric(key)) {
                numResults += 1;
            }
        });
        if (numResults > 1) {
            $("#multiUsersFoundModal").show();
            for (var x = 0; x < numResults; x++) {
                $("#multiUsersFoundTable > tbody:last").append("<tr class=\"multiUserFoundResult\"><td>" + result[x].first_name + "</td><td>" +
                    result[x].last_name + "</td><td>" + result[x].email + "</td></tr>");

                console.log(result[x]);
            }

            $(".multiUserFoundResult").click(function (event) {
                console.log($(event.target).parent());
                var firstName = $(event.target).parent().children('td').eq(0).html();
                var lastName = $(event.target).parent().children('td').eq(1).html();
                var email = $(event.target).parent().children('td').eq(2).html();
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

    $("#userNotFoundModalClose").click(function (event) {
        $("#userNotFoundModal").hide();
    });

    $("#newCustomerModalClose").click(function (event) {
        $("#newCustomerModal").hide();
    });

    var checkUsernameInUse = function(username) {
        var result;
        $.ajax({
            url: "/users/"+username,
            async: false,
            type: 'GET',
            statusCode: {
                404: function() {
                    steal.dev.log("FREE!");
                    result = false;
                },
                200: function() {
                    steal.dev.log("NOT FRE!");
                    result = true;
                }
            }
        })
        return result;
    };

    var showUserAddedAlert = function(target) {
        var alert = '<div class="alert alert-success" id="userCreatedAlert">' +
                        '<a class="close" data-dismiss="alert">x</a>' +
                        '<p>User was successfully created!</p>' +
                        '</div>'
        $(target).prepend(alert);
    }

    $("body").on("click", "#newCustomerModalCreate", function (event) {
        /**
         * This function tries to create a new user. It contains code to try to find an unused username. It does this
         * by trying the first part of their e-mail address, then the first letter of their first name and their last
         * name, and finally by appending a number to the end of their first letter and lastname and incrementing it
         * until the server doesn't find a user with that username.
         * @type {*|jQuery}
         */
        // TODO: Validation?
        var firstName = $("#newCustomerFirstNameInput").val();
        var lastName = $("#newCustomerFirstNameInput").val();
        var email = $("#newCustomerEmailInput").val();
        // First we are going to do need to generate a username that does not exist. Let's start with their e-mail.
        var username = email.split("@", 1)[0];
        steal.dev.log("Starting with checking: " + username);
        User.findOne({OneName: username}, function (result) {
            // We'll combine the first letter of their username with their last name
            // TODO: Should we restrict length?
            var username = firstName[0] + lastName.slice(1);
            steal.dev.log("Trying: " + username);
            User.findOne({OneName: username}, function (result) {
                // If we are here, we're giving up and just going to take
                // the first letter of their first name and their last name
                // and append an ever increasing number to it until we find one
                // that is not used.
                var curNum = 1;
                var username = firstName[0] + lastName.slice(1);
                // Need to keep a root copy of the username
                var rootUsername = username;
                username = rootUsername+curNum.toString();
                var inUse = checkUsernameInUse(username);
                steal.dev.log("inUse is: "+inUse);
                // Iterate while the server returns a user found result
                while (checkUsernameInUse(username)) {
                    curNum += 1;
                    // Generate a new username
                    username = rootUsername+curNum.toString();
                    steal.dev.log("Trying username: "+username)
                }
                // Once we are here, we know the server has returned a 404, so we can use that username!

                // Generate a new user
                var newUser = new User({username: username, first_name: firstName, last_name: lastName,
                                        password: "password", email: email});
                // Save it to the server
                newUser.save(function (saved) {
                    steal.dev.log("New user saved!");
                    showUserAddedAlert($("#newCustomerModal .modal-body"));
                });
            }, function (result) {
                // If we are here, we know that we can use the first letter and last name
                var newUser = new User({username: username, first_name: firstName, last_name: lastName,
                    password: "password", email: email});
                newUser.save(function (saved) {
                    steal.dev.log("New user saved!");
                    showUserAddedAlert($("#newCustomerModal .modal-body"));
                });
            })

        }, function (result) {
            // If here, we know that we can use the first part of their e-mail address!
            var newUser = new User({username: username, first_name: firstName, last_name: lastName,
                password: "password", email: email});
                newUser.save(function (saved) {
                showUserAddedAlert($("#newCustomerModal .modal-body"));
            });
        });
    });


    $("#mainrow").on("click", "#newReservationFindCustomerBtn", function (event) {
        /**
         * This function handles trying to find a customer based on what they entered into
         * the form.
         */
        event.preventDefault();
        // Let's search by their e-mail first

        if ($("#customerEmail").val()) {
            User.findOne({id: $("#customerEmail").val()}, function (User) {
                populateInfo(User);
            }, function () {
                $("#userNotFoundModal").show();
            });
            // If no e-mail was entered, let's search by first and last name if they entered both
        } else if ($("#customerFirstName").val() && $("#customerLastName").val()) {
            User.findOne({FullName: $("#customerFirstName").val() + " " + $("#customerLastName").val()}, function (User) {
                populateInfo(User);
            }, function () {
                $("#userNotFoundModal").show();
            });
            // Finally, let's search by first name or last name if they only entered one
        } else if (($("#customerFirstName").val() || $("#customerLastName").val())) {
            if ($("#customerFirstName").val()) {
                oneName = $("#customerFirstName").val();
            } else if ($("#customerLastName")) {
                oneName = $("#customerLastName").val();
            }
            User.findOne({OneName: oneName}, function (User) {
                populateInfo(User);
            }, function () {
                $("#userNotFoundModal").show();
            });
        }
        $("#userNotFoundModalClose").click(function () {
            $("#userNotFoundModal").hide();
        });
    });

    $("#mainrow").on("click", "#newReservationNewCustomerBtn", function (event) {
        /**
         * This function handles adding a new customer to the system.
         */
        event.preventDefault();
        $("#newCustomerModal").show();

    });

    $("#mainrow").on("click", "#addNewActionBtn", function (event) {
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

        $("#newReservationActions").append('<div class="well reservationActionDiv" data-actiontype="' + actionType + '" data-origin="' + actionOrigin + '" data-destination="' + actionDestination + '" data-start="' + actionStart + '" data-end="' + actionEnd + '"><button type="button" class="btn btn-danger btn-xs pull-right del-action-btn"><span class="glyphicon glyphicon-remove"></span></button><div><font size=6>' + actionTypeName + '</font><br /><font size=2>Between ' + actionStart + ' and ' + actionEnd + '</font><br /><font size=4>From ' + actionOriginName + ' to ' + actionDestinationName + '<br />Equipment:</font><br /><ul id="equipmentList"><li>Item 1</li></ul></div>' + '<div class="equipmentAssignedToActionDiv"></div></div>');
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

    $("#mainrow").on("click", ".del-action-btn", function (event) {
        /**
         * This function handles deleting an action from a reservation.
         */
        steal.dev.log("Deleting an action");
        $(this).parent().remove();
    });

    $("#mainrow").on("click", "#showAddEquipmentModalBtn", function (event) {
        /**
         * This button handles displaying the modal window to add new equipment to
         * a reservation
         */
        steal.dev.log("Bringing up add equipment modal");
        $("#addEquipmentModal").modal('show');
        $("#newReservationActions").children("#individualAction").each(function () {
            steal.dev.log(jQuery.data($(this), "actiontype"));
        });
        $("#applyToAllActionsChkDiv").append('<br /><input type="checkbox" id="testActionBox" value="applyToTestAction" checked/>Test action')
    });

    $("#mainrow").on("click", "#addEquipmentBtn", function (event) {
        /**
         * This button handles searching the server for an inventory item and adding it to
         * a reservation.
         */
        var invItemId = $("#equipmentId").val();

        steal.dev.log("Searching for equipment ID: " + invItemId);
        InventoryItem.findOne({id: invItemId}, function (success) {
            steal.dev.log("Found an item");
            console.log(success);
            $("#newReservationEquipment").append('<div class="equipmentEntry well">#' + success.ItemID + ' ' + success.Description + '</div>');
            $('.reservationActionDiv .equipmentAssignedToActionDiv').each(function (index) {
                steal.dev.log('Appending equipment to Action');
                $(this).append('<div class="equipmentForAction" id="equipmentForAction-' + success.ItemID + '">#' + success.ItemID + ' ' + success.Description +
                    '<button type="button" class="removeEquipmentFromActionBtn btn btn-xs btn-danger pull-right">Remove</button>' +
                    '</div>');
            });

            $("#addEquipmentModal").modal('hide');
        }, function (error) {
            $(".alert-equipment-not-found").hide();
            $("#addEquipmentModalBody").prepend('<div class="alert alert-danger alert-dismissable alert-equipment-not-found">' +
                '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
                '<strong>Error!</strong> An item with that ID was not found! Please try again.' +
                '</div>');
        });
    });

    $("#mainrow").on("click", "#createReservationBtn", function(event) {
       event.preventDefault();
        steal.dev.log("Creating a new reservation")
        var customerStatus = "SomeStatus"
        var eventTitle = $("#newReservationEventTitle").val();
        var customerPhone = $("#customerPhone").val();
        var customerEmail = $("#customerEmail").val();
        var customerDept = "SomeDept";
        var reservationNotes = $("#newReservationNotes").val();
        var ownerID = 1;
        var customerID = 2;
        var newReservation = new Reservation({CustomerStatus: customerStatus,
                                                EventTitle: eventTitle,
                                                CustomerPhone: customerPhone,
                                                CustomerEmail: customerEmail,
                                                CustomerDept: customerDept,
                                                ReservationNotes: reservationNotes,
                                                OwnerID: ownerID,
                                                CustomerID: customerID});
        //newReservation.save();
        $(".reservationActionDiv").each(function() {

            var formattedStartDate = new Date($(this).data('start'));
            var formattedEndDate = new Date($(this).data('end'));
            var startYear = formattedStartDate.getFullYear()
            var startMonth = formattedStartDate.getMonth()
            startMonth += 1
            var startDay = formattedStartDate.getDay()
            var startMinute = formattedStartDate.getMinutes()
            var startHour = formattedStartDate.getHours()

            var endYear = formattedEndDate.getFullYear()
            var endMonth = formattedEndDate.getMonth()
            endMonth += 1
            var endDay = formattedEndDate.getDay()
            var endMinute = formattedEndDate.getMinutes()
            var endHour = formattedEndDate.getHours()
            steal.dev.log("OK, creating new action");
            var newAction = new Action({
                StartTime: startYear+"-"+startMonth+"-"+startDay+"T"+startHour+":"+startMinute,
                EndTime: endYear+"-"+endMonth+"-"+endDay+"T"+endHour+":"+endMinute,
                Origin: $(this).data("origin"),
                Destination: $(this).data("destination"),
                ActionTypeID: $(this).data("actiontype"),
                Reservation: newReservation.ReservationID,
                AssignedOperatorID: null,
                ActionNotes: $(this).find(".actionNotes").val(),
                ActionStatus: $(this).find(".actionStatus").val()
            });
            steal.dev.log("Done creating new action. Saving...");
            newAction.save(function() {
                steal.dev.log("Saved!");
            });
            steal.dev.log("Done saving");
        });


    });
})