steal(function() {
    $("#mainrow").on("click", "#createNewStatusFormLink", function(event) {
        /**
         * This function handles displaying the create new status form
         */
        $("#administerStatusesDiv").load("/addNewStatusForm/", function() {

        });

    });
    $("#mainrow").on("click", "#chooseStatusToEditLink", function(event) {
        /**
         * This function handles displaying the edit new status form
         */
        $("#administerStatusesDiv").load("/chooseStatusToEditForm/", function() {
            updateStatusSelect();


        });
    });

    var updateStatusSelect = function() {
        // Here we are going to get the list of statuses to populate
        $("#existingStatusNameSelect").empty();
        $("#existingStatusNameSelect").append("<option value='None' selected='selected'>Choose a Status...</option>");
        $.getJSON("/statuses/", function(data) {

                // This populates the dropdown to let people choose a status to edit
                $.each(data, function(key, value) {
                    // If we had one selected prior, remember to restore that one as the selected one
                    $("#existingStatusNameSelect").append("<option value='"+value.StatusID+"'>"+value.StatusName+"</option>");

                });
        });
    }

    var updateEditStatusForm = function(status) {
        $("#existingStatusName").val(status.StatusName);
        $("#existingStatusDescription").val(status.StatusDescription);
    };

    $("#mainrow").on("change", "#existingStatusNameSelect", function() {
        /**
         * This function handles form pre-population when they choose a status from
         * the drop down.
         */
        var selectedStatusID = $("#existingStatusNameSelect").val();
        // This is to handle them choosing the "Choose a Status..." option in the dropdown
        if (selectedStatusID == "None") {
            return;
        }
        // When they choose an existing status from the dropdown, we want to pre-populate the form
        // with existing values
        var status = $.getJSON("/statuses/"+selectedStatusID, function(response) {
            updateEditStatusForm(response)
        });
    });

    $("#mainrow").on("click", "#submitChooseStatusToEditBtn", function(event) {
        event.preventDefault();
        var selectedStatusID = $("#existingStatusNameSelect").val();

        // Here we create a Model for the particular Status we want to edit. We retrieve the Status
        // from the server with a matching ID to the one in the drop down.
        // Even though the server side model doesn't have id, it has StatusID, we have to set an id
        // property on the client side model so that it knows to use PUT, not POST.
        Status.findOne({id: selectedStatusID}, function(status) {
            status.attr("id", selectedStatusID);
            // Change the fields...
            status.attr("StatusName", $("#existingStatusName").val());
            status.attr("StatusDescription", $("#existingStatusDescription").val());
            // Save to the server
            status.save(function(saved) {
                $("#editStatusFormBody").prepend("<div id='editStatusSuccessAlert' class='alert alert-success'>Status Updated!</div>");
                updateEditStatusForm(saved);
                updateStatusSelect();
            });

        });

    });

    $("#mainrow").on("click", "#deleteStatusBtn", function(event) {
        /**
         * This function handles the pressing of the Delete button when someone wants to delete
         * a status. It will show a confirmation alert.
         */
        event.preventDefault();

        if ($("#existingStatusNameSelect").val() == "None") {
            return;
        }
        $("#editStatusFormBody").prepend("<div id='deleteStatusConfirmationAlert' class='alert alert-danger'>" +
            "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
            "<h4 id='confirmDeleteMsg'>Are you sure you want to delete that status?</h4>" +
            "<p><button id='confirmDeleteStatusBtn' type='button' class='btn btn-danger'>Yes, delete</button>&nbsp&nbsp</div>");
    });

    $("#mainrow").on("click", "#confirmDeleteStatusBtn", function(event) {
        /**
         * This function handles the pressing of the confirm deletion button. It actually deletes the
         * object from the server.
         */
        var selectedStatusID = $("#existingStatusNameSelect").val();
        Status.findOne({id: selectedStatusID}, function(status) {
            status.attr("id", selectedStatusID);
            status.destroy(function() {
                            updateStatusSelect();
                            $("#confirmDeleteMsg").html("Status deleted!");
                            $("#confirmDeleteStatusBtn").hide();
                            $("#existingStatusName").val("");
                            $("#existingStatusDescription").val("");
            });

        });
    });
    
    $("#mainrow").on("click", "#submitCreateNewStatusBtn", function(event) {
        /**
         * This function handles the pressing of the create new status button
         */
            event.preventDefault();
        var newStatus = new Status({StatusName: $("#newStatusNameInput").val(),
                            StatusDescription: $("#newStatusDescriptionInput").val()
                            });
        newStatus.save(function(saved) {
            $("#addNewStatusFormBody").prepend("<div id='addStatusConfirmationAlert' class='alert alert-success'>" +
            "<h4>Status added!</h4></div>");
            $("#addStatusConfirmationAlert").fadeOut(8000);
            $("#newStatusNameInput").val("");
            $("#newStatusDescriptionInput").val("");
        });
    });
});