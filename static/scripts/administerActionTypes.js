steal(function() {
    $("#mainrow").on("click", "#createNewActionTypeFormLink", function(event) {
        /**
         * This function handles displaying the create new ActionType form
         */
        $("#administerActionTypesDiv").load("/addNewActionTypeForm/", function() {

        });

    });
    $("#mainrow").on("click", "#chooseActionTypeToEditLink", function(event) {
        /**
         * This function handles displaying the edit new ActionType form
         */
        $("#administerActionTypesDiv").load("/chooseActionTypeToEditForm/", function() {
            updateActionTypeSelect();


        });
    });

    var updateActionTypeSelect = function() {
        // Here we are going to get the list of ActionTypes to populate
        $("#existingActionTypeNameSelect").empty();
        $("#existingActionTypeNameSelect").append("<option value='None' selected='selected'>Choose an ActionType...</option>");
        $.getJSON("/actions/", function(data) {

                // This populates the dropdown to let people choose a ActionType to edit
                $.each(data, function(key, value) {
                    // If we had one selected prior, remember to restore that one as the selected one
                    $("#existingActionTypeNameSelect").append("<option value='"+value.ActionTypeID+"'>"+value.ActionTypeName+"</option>");

                });
        });
    }

    var updateEditActionTypeForm = function(ActionType) {
        $("#existingActionTypeName").val(ActionType.ActionTypeName);
        $("#existingActionTypeCode").val(ActionType.ActionTypeCode);
    };

    $("#mainrow").on("change", "#existingActionTypeNameSelect", function() {
        /**
         * This function handles form pre-population when they choose a ActionType from
         * the drop down.
         */
        var selectedActionTypeID = $("#existingActionTypeNameSelect").val();
        // This is to handle them choosing the "Choose a ActionType..." option in the dropdown
        if (selectedActionTypeID == "None") {
            return;
        }
        // When they choose an existing ActionType from the dropdown, we want to pre-populate the form
        // with existing values
        var ActionType = $.getJSON("/actions/"+selectedActionTypeID, function(response) {
            updateEditActionTypeForm(response)
        });
    });

    $("#mainrow").on("click", "#submitChooseActionTypeToEditBtn", function(event) {
        event.preventDefault();
        var selectedActionTypeID = $("#existingActionTypeNameSelect").val();

        // Here we create a Model for the particular ActionType we want to edit. We retrieve the ActionType
        // from the server with a matching ID to the one in the drop down.
        // Even though the server side model doesn't have id, it has ActionTypeID, we have to set an id
        // property on the client side model so that it knows to use PUT, not POST.
        ActionType.findOne({id: selectedActionTypeID}, function(ActionType) {
            ActionType.attr("id", selectedActionTypeID);
            // Change the fields...
            ActionType.attr("ActionTypeName", $("#existingActionTypeName").val());
            ActionType.attr("ActionTypeCode", $("#existingActionTypeCode").val());
            // Save to the server
            ActionType.save(function(saved) {
                $("#editActionTypeFormBody").prepend("<div id='editActionTypeSuccessAlert' class='alert alert-success'>ActionType Updated!</div>");
                updateEditActionTypeForm(saved);
                updateActionTypeSelect();
            });

        });

    });

    $("#mainrow").on("click", "#deleteActionTypeBtn", function(event) {
        /**
         * This function handles the pressing of the Delete button when someone wants to delete
         * a ActionType. It will show a confirmation alert.
         */
        event.preventDefault();

        if ($("#existingActionTypeNameSelect").val() == "None") {
            return;
        }
        $("#editActionTypeFormBody").prepend("<div id='deleteActionTypeConfirmationAlert' class='alert alert-danger'>" +
            "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
            "<h4 id='confirmDeleteMsg'>Are you sure you want to delete that ActionType?</h4>" +
            "<p><button id='confirmDeleteActionTypeBtn' type='button' class='btn btn-danger'>Yes, delete</button>&nbsp&nbsp</div>");
    });

    $("#mainrow").on("click", "#confirmDeleteActionTypeBtn", function(event) {
        /**
         * This function handles the pressing of the confirm deletion button. It actually deletes the
         * object from the server.
         */
        var selectedActionTypeID = $("#existingActionTypeNameSelect").val();
        ActionType.findOne({id: selectedActionTypeID}, function(ActionType) {
            ActionType.attr("id", selectedActionTypeID);
            ActionType.destroy(function() {
                            updateActionTypeSelect();
                            $("#confirmDeleteMsg").html("ActionType deleted!");
                            $("#confirmDeleteActionTypeBtn").hide();
                            $("#existingActionTypeName").val("");
                            $("#existingActionTypeCode").val("");
            });

        });
    });
    
    $("#mainrow").on("click", "#submitCreateNewActionTypeBtn", function(event) {
        /**
         * This function handles the pressing of the create new ActionType button
         */
            event.preventDefault();
        var newActionType = new ActionType({ActionTypeName: $("#newActionTypeNameInput").val(),
                            ActionTypeCode: $("#newActionTypeCodeInput").val()
                            });
        newActionType.save(function(saved) {
            $("#addNewActionTypeFormBody").prepend("<div id='addActionTypeConfirmationAlert' class='alert alert-success'>" +
            "<h4>ActionType added!</h4></div>");
            $("#addActionTypeConfirmationAlert").fadeOut(8000);
            $("#newActionTypeNameInput").val("");
            $("#newActionTypeCodeInput").val("");
        });
    });
});