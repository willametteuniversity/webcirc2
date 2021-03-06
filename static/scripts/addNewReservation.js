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


    var checkUsernameInUse = function (username) {
        /**
         * This function checks if a username is in use on the server
         */
        var result;
        $.ajax({
            url: "/users/" + username,
            async: false,
            type: 'GET',
            statusCode: {
                404: function () {
                    steal.dev.log("FREE!");
                    result = false;
                },
                200: function () {
                    steal.dev.log("NOT FREE!");
                    result = true;
                }
            }
        })
        return result;
    };

    var showUserAddedAlert = function (target) {
        /**
         * This function displays a user added alert
         * @type {string}
         */
        var alert = '<div class="alert alert-success" id="userCreatedAlert">' +
            '<a class="close" data-dismiss="alert">x</a>' +
            '<p>User was successfully created!</p>' +
            '</div>'
        $(target).prepend(alert)
    };

    var showReservationCreatedAlert = function (target) {
        /**
         * This function displays a reservation created alert
         * @type {string}
         */
        var alert = '<div class="alert alert-success">' +
            '<a href="#" class="close" data-dismiss="alert">&times;</a>' +
            '<strong>Success!</strong> A reservation was successfully created.' +
            'Please add Actions now</div>';
        $(target).prepend(alert);
    };

    var showReservationCreationError = function (target) {
        /**
         * This function displays a reservation creation error
         * @type {string}
         */
        var alert = '<div class="alert alert-success">' +
            '<a href="#" class="close" data-dismiss="alert">&times;</a>' +
            '<strong>Success!</strong> A reservation was successfully created.' +
            'Please add Actions now</div>';
        $(target).prepend(alert);
    };

    var clearActionForm = function () {
        /**
         * This function clears all the fields in the Action form. It is meant to be called
         * after an action is added, so that the user has a blank form to add another.
         */
        steal.dev.log('Clearing Action form');
        $('#startDateTimePicker').val('');
        $('#endDateTimePicker').val('');
        $('#actionNote').val('')
    };

    var clearCustomerForm = function () {
        /**
         * This function clears all the fields in the Customer form
         */
        steal.dev.log('Clearing Customer form');
        $('#customerFirstName').val('');
        $('#customerLastName').val('');
        $('#customerPhone').val('');
        $('#customerEmail').val('');
    };

    var clearReservationForm = function () {
        /**
         * This function clears all the fields in the Reservation form
         */
        steal.dev.log('Clearing Reservation form');
        $('#newReservationEventTitle').val('');
        $('#newReservationNotes').val('');
    };

    var clearActions = function () {
        /**
         * This function removes the actions added (i.e., deletes the divs) so they don't get
         * processed if they add another reservation
         */
        $('.reservationActionDiv').remove();
    };

    var addEquipmentToAction = function (item) {
        $('#newReservationEquipment').append('<div class="equipmentEntry well">#'+item.ItemID+' '+item.Description+'</div>');
        // TODO: Check if item is already added? 
        // If the all actions box is checked, no need for anything else,
        // just iterate over every action div to add the equipment 
        if ($("#applyToAllActionsChk").is(":checked")) {
            $('.reservationActionDiv').each(function (index, value) {
                $(this).append('<div class="equipmentForAction" id="equipmentForAction-' + item.ItemID + '">#' +
                item.ItemID + ' ' + item.Description +'<button type="button" class="removeEquipmentFromActionBtn'+

                'btn btn-xs btn-danger pull-right">Remove</button>' + '</div>');
            });
        } else {
            // If only a few check boxes are checked (not the All Actions one), then we need to find out which action divs 
            // are desired, iterate over them, and append the equipment 
            // Here we use the uniqueId we generated for the action Divs earlier 
            $('.addEquipmentActionCheck:checked').each(function (index) {
                steal.dev.log('Appending equipment to Action');
                $('#' + $(this).data('actiondivid')).append('<div class="equipmentForAction" id="equipmentForAction-' +
                item.ItemID + '">#' + item.ItemID + ' ' + item.Description +
                '<button type="button" class="removeEquipmentFromActionBtn btn btn-xs btn-danger pull-right">Remove</button>' +
                '</div>');
            });
        };
        $("#addEquipmentModal").modal('hide');
    };

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
                username = rootUsername + curNum.toString();
                var inUse = checkUsernameInUse(username);
                steal.dev.log("inUse is: " + inUse);
                // Iterate while the server returns a user found result
                while (checkUsernameInUse(username)) {
                    curNum += 1;
                    // Generate a new username
                    username = rootUsername + curNum.toString();
                    steal.dev.log("Trying username: " + username)
                }
                // Once we are here, we know the server has returned a 404, so we can use that username!

                // Generate a new user
                var newUser = new User({
                    username: username, first_name: firstName, last_name: lastName,
                    password: "password", email: email
                });
                // Save it to the server
                newUser.save(function (saved) {
                    steal.dev.log("New user saved!");
                    showUserAddedAlert($("#newCustomerModal .modal-body"));
                });
            }, function (result) {
                // If we are here, we know that we can use the first letter and last name
                var newUser = new User({
                    username: username, first_name: firstName, last_name: lastName,
                    password: "password", email: email
                });
                newUser.save(function (saved) {
                    steal.dev.log("New user saved!");
                    showUserAddedAlert($("#newCustomerModal .modal-body"));
                });
            })

        }, function (result) {
            // If here, we know that we can use the first part of their e-mail address!
            var newUser = new User({
                username: username, first_name: firstName, last_name: lastName,
                password: "password", email: email
            });
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
        $("#newActionForm").validate();
        var isValid = $("#newActionForm").valid();
        if (isValid == false) {
            steal.dev.log("New Action Form is not valid");
            return;
        }
        steal.dev.log("New Action Form is valid, proceeding...");
        // We'll need these various attributes to create the action div
        // Type of action given as the ID it has on the erver
        var actionType = $("#actionType").val();
        // Textual representation of the actionType (delivery, pickup, etc)
        var actionTypeName = $("#actionType option:selected").text();
        // User that was assigned to the action
        var actionAssignedUser = $("#actionAssignedUser").val();
        // Starting time of the action
        // TODO: Should this be changed to represent the earliest/latest concept?
        var actionStart = $("#startDateTime").data('date');
        // Latest time of the action
        // TODO: Should this be changed to represent the earliest/latest concept?
        var actionEnd = $("#endDateTime").data('date');
        var formattedStartDate = new Date(actionStart);
        var formattedEndDate = new Date(actionEnd);
        var startYear = formattedStartDate.getFullYear();
        var startMonth = formattedStartDate.getMonth();
        // javascript months are 0-11 for some reason
        startMonth += 1;
        var startDay = formattedStartDate.getDate();
        var startMinute = formattedStartDate.getMinutes();
        var startHour = formattedStartDate.getHours();

        var endYear = formattedEndDate.getFullYear();
        var endMonth = formattedEndDate.getMonth();
        endMonth += 1;
        var endDay = formattedEndDate.getDate();
        var endMinute = formattedEndDate.getMinutes();
        var endHour = formattedEndDate.getHours();
        // Origin of the action in the form of the ID of the model on the server
        var actionOrigin = $("#actionOrigin").val();
        // Textual name of the action origin
        var actionOriginName = $("#actionOrigin option:selected").text();
        // ID of destination Location on server, then textual
        var actionDestination = $("#actionDestination").val();
        var actionDestinationName = $("#actionDestination option:selected").text();
        // Any notes specific to that action
        var actionNote = $("#actionNote").val();
        // Finally, we're going to append a new action to the newReservationActions div on the right to display them to the user
        // We are going to populate a bunch of data- attributes for user later
        // We also give it a unique ID so we can tell which checkbox is linked to which action div in the add equipment
        // form

        var timezone = '-06:00'
        var newAction = new Action({
            StartTime: startYear + "-" + startMonth + "-" + startDay + "T" + startHour + ":" + startMinute + timezone,
            EndTime: endYear + "-" + endMonth + "-" + endDay + "T" + endHour + ":" + endMinute + timezone,
            Origin: actionOrigin,
            Destination: actionDestination,
            ActionTypeID: actionType,
            Reservation: newReservation.ReservationID,
            AssignedOperatorID: actionAssignedUser,
            ActionNotes: actionNote,
            ActionState: "1",
        });
        newAction.save(function (saved) {
            steal.dev.log("New action created...");
            steal.dev.log(saved);
            $("#newReservationActions").append($('<div class="well reservationActionDiv" data-actionid="' +
            saved.ActionID + '" data-origintext="' + actionOriginName + '" data-destinationtext="' + actionDestinationName +
            '" data-actiontypetext="' + actionTypeName + '"><button type="button" class="' + 'btn btn-danger btn-xs pull-right del-action-btn">' +
            '<span class="glyphicon glyphicon-remove"></span></button><div><font size=6>'
            + actionTypeName + '</font><br /><font size=2>Between ' + actionStart + ' and ' + actionEnd
            + '</font><br /><font size=4>From ' + actionOriginName + ' to ' + actionDestinationName
            + '<br />Equipment:</font><br /><ul class="equipmentList"></ul></div>'
            + '<div class="equipmentAssignedToActionDiv"></div></div>'));
            clearActionForm();
            $("#showAddEquipmentModalBtn").button("enable");
        }, function (error) {
            // Need to display this to the user somehow...
            steal.dev.log("There was an error creating the action")
            steal.dev.log("Error was" + error.responseText)
        });


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
        var actionID = $(this).parent().data('actionid');
        console.log(actionID);
        Action.findOne({id: actionID}, function(Action) {
            Action.attr("id", actionID);
            // TODO: Something to handle failing to delete?
            Action.destroy();
            console.log("Removing...");
            $(this).parent().remove();
        }, function(failure) {
            // TODO: Do something intelligent on failure here
        });

    });

    $("#mainrow").on("click", "#showAddEquipmentModalBtn", function (event) {
        /**
         * This button handles displaying the modal window to add new equipment to
         * a reservation
         */
        steal.dev.log("Bringing up add equipment modal");

        // Clear the current checkboxes, as we want to regenerate them in case the actions have changed
        $(".addEquipmentActionCheck").remove();
        $(".addEquipmentToActionCheckSpan").remove();

        $('#equipmentDisplayByLabelList').empty();
        $('#equipmentDisplayByCategoryDiv').empty();
        $('#equipmentDisplayByCategoryDiv').append('<div id="equipmentDisplayByTree"></div>');
        $("#addEquipmentModal").modal('show');
        // Now we want to iterate over every action that has been added to build the checkbox list
        $.each($(".reservationActionDiv"), function (index, value) {
            steal.dev.log("Iterating over existing actions");
            // We need this data to build the text for the checkbox
            var actionTypeText = $(this).data("actiontypetext");
            var actionOriginText = $(this).data("origintext");
            var actionDestinationText = $(this).data("destinationtext");
            var actionDivId = $(this).data("actionid");
            // We need to construct a meaningful string to identify the action this checkbox applies to
            var actionDescString = ' <span class="addEquipmentToActionCheckSpan">' + actionTypeText + ' from ' + actionOriginText + ' to ' + actionDestinationText + '</span>'
            // Now append the HTML for the checkbox
            $("#applyToAllActionsChkDiv").append('<div><input data-actionchkid="' + actionDivId + '" class="addEquipmentActionCheck" type="checkbox" value="applyToTestAction" />' + actionDescString + "</div>");
        });
    });

    var addSpecificEquipment = function(equipmentID) {
        /**
         * This function attempts to add a specific piece of equipment by ID. It is used when the operator attempts to
         * add a specific piece of equipment to a reservation as opposed to letting the server select equipment from a
         * category.
         */


    };
    var addEquipment = function(categoryID) {
        var actions = [];
        var equipmentType = $('#equipmentTypeDropdown').val();
        steal.dev.log('Beginning addEquipment of '+categoryID);
        $.each($('.reservationActionDiv'), function(key, value) {
            console.log($(this).data('actionid'));
            actions.push($(this).data('actionid'));
        });

        var equipmentUrl = '/findAvailableEquipment/';

        $.getJSON(equipmentUrl, {'actions[]': actions, 'categoryid': categoryID}, function(result) {
            $.each(result, function(key, value) {
                var actionChk = $('*[data-actionchkid="'+key+'"]').next();
                var curText = actionChk.text();
                var allSucceeded = true;
                if (value[0] == false) {
                    curText += ' No equipment available'
                    allSucceeded = false;
                } else {
                    curText += ' Assigned equipment: '+value[1]
                }
                actionChk.text(curText)
            });

        });
    };

    $("#mainrow").on("click", "#addEquipmentBtn", function (event) {
        /**
         * This button handles searching the server for an inventory item and adding it to
         * a reservation.
         */
        console.log('Attempting to add equipment...');

        var equipmentType = $('#equipmentTypeDropdown').val();
        if (equipmentType == 'inventory') {
            var currentTreeSelectText = $('#equipmentDisplayByTree').jstree().get_text($('#equipmentDisplayByTree').jstree().get_selected());
            if (currentTreeSelectText[0] == "#") {
                console.log('Specific item selected!');
                var specificID = currentTreeSelectText.split(" ")
                specificID = specificID[0];
                specificID = specificID.replace("#","");
                addSpecificEquipment(specificID);
            } else {
                addEquipment($('#equipmentDisplayByTree').jstree().get_selected()[0]);
            }
        } else {
            var equipmentTerm = $("#equipmentTerm").val();
            Label.findOne({LabelName: equipmentTerm}, function(success) {
                addEquipment(success.LabelID);
            }, function(failure) {
                // TODO: This should display a warning to the user about no items being found?
                steal.dev.log("No label found");
            });
        }

    });

    $('#mainrow').on('keyup', '#equipmentTerm', function (event) {
        event.preventDefault();
        $(".labeled-equipment").remove();
        console.log(event);
        if (event.keyCode == 13) {
            var equipmentTerm = $("#equipmentTerm").val();
            steal.dev.log('Equipment term is: ' + $('#equipmentTerm').val());
            if ($.isNumeric(equipmentTerm)) {
                // TODO: We need to actually check that the piece of equipment is available here
                InventoryItem.findOne({id: equipmentTerm}, function (item) {
                    addEquipmentToAction(item);
                });
            } else {
                // Let's try to find a Label that matches
                steal.dev.log('Searching for a label...');
                // TODO: We should probably remove the category selector drop down entirely
                    InventoryItem.findAll({eterm: equipmentTerm}, function (items) {
                        $.each(items, function (index, value) {
                            var descString = '#' + value.ItemID + ' ';
                            ItemBrand.findOne({id: value.BrandID}, function (brand) {
                                descString += brand.BrandName;
                                ItemModel.findOne({id: value.ModelID}, function (model) {
                                    descString += ' ' + model.ModelDesignation;
                                    steal.dev.log('DescString is: ' + descString);
                                    $('#equipmentDisplayByLabelList').append('<a href="#" class="list-group-item labeled-equipment">' + descString + '</a>');
                                })
                            });
                        });
                    });
                    $('#equipmentDisplayByTree').empty().jstree('destroy');
                    steal.dev.log('Populating jsTree');
                    // OK, now let's populate the tree on the other side...
                    var actions = [];
                    $.each($('.reservationActionDiv'), function(key, value) {
                        actions.push($(this).data('actionid'));
                    });
                    $("#equipmentDisplayByTree").jstree({
                        'core': {
                            'data': {
                                'url': '/categoryHierarchyWithEquipment/?term=' + equipmentTerm + '&actions[]='+JSON.stringify(actions)
                            },
                            'check_callback': true

                        },
                        'plugins': ['dnd']
                    });

            }
        }
    });

    $("#mainrow").on("click", ".removeEquipmentFromActionBtn", function (event) {
        /**
         * This handles remove a piece of equipment from an action
         */
        steal.dev.log($(this).prev());
        $(this).closest(".equipmentForAction").remove();
    });

    $("#mainrow").on("click", "#createReservationBtn", function (event) {
        /**
         * This function handles creating the reservation with its associated actions and pieces of equipment
         */

        var isValid = false;
        steal.dev.log("Validating forms..");
        $("#newReservationCustomerForm").validate();
        isValid = $("#newReservationCustomerForm").valid();
        if (isValid == false) {
            return;
        }
        $("#newReservationForm").validate();
        isValid = $("#newReservationForm").valid()
        if (isValid == false) {
            return;
        }

        steal.dev.log("Forms are valid, proceeding...");
        var customerStatus = "SomeStatus";
        var eventTitle = $("#newReservationEventTitle").val();
        var customerPhone = $("#customerPhone").val();
        var customerEmail = $("#customerEmail").val();
        var customerDept = "SomeDept";
        var reservationNotes = $("#newReservationNotes").val();

        // TODO: Fix these to be lookups
        var ownerID = 1;
        var customerID = 2;

        newReservation = new Reservation({
            CustomerStatus: customerStatus,
            EventTitle: eventTitle,
            CustomerPhone: customerPhone,
            CustomerEmail: customerEmail,
            CustomerDept: customerDept,
            ReservationNotes: reservationNotes,
            OwnerID: ownerID,
            CustomerID: customerID
        });

        newReservation.save(function (saved) {
            // Now we can allow them to add actions
            $("#addNewActionBtn").button("enable");
            // Want to disable the Create Reservation button so they don't accidentally make more
            $("#createReservationBtn").attr('disabled', 'disabled');
            // Display a reservation created message
            showReservationCreatedAlert($("#newReservationForm"));
        }, function (error) {
            $("#addingReservationErrorMessageDiv").html(error.responseText);
            $("#errorAddingReservationModal").modal('show');

        });
    });

    $("#mainrow").on("click", "#acknowledgeReservationSuccessfullyAddedBtn", function (event) {
        event.preventDefault();
        clearActionForm();
        clearCustomerForm();
        clearReservationForm();
        clearActions();
        $('#reservationAddedSuccessfullyModal').modal('hide');

    });

});


/**
 a1.res = res1
 a2.res = res1

 newResStart = firstActionLeavingHome
 newResEnd = lastResActionReturningHome

 nearestResStartPast = action where action.res == res1 && e leaves home && is nearest in time to newResStart && occurs before newResStart
 nearestResEnd = action where action.res == res1 and e returns home

 if no action where e leaves home occurs between newResStart / newResEnd AND
 no action where e returns home occurs between newResStart / newResEnd AND
 newResStart is before nearestResEnd
 */



