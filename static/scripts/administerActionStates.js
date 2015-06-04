steal(function() {
    $("#mainrow").on("click", "#createNewActionStateFormLink", function(event) {
        /**
         * This function handles displaying the create new status form
         */
        $("#administerActionStatesDiv").load("/addNewActionStateForm/", function() {
             $(':checkbox').checkboxpicker();
        });

    });
    $("#mainrow").on("click", "#chooseActionStateToEditLink", function(event) {
        /*
         * This function handles displaying the edit new status form
         */
        $("#administerActionStatesDiv").load("/chooseActionStateToEditForm/", function() {
            $(':checkbox').checkboxpicker();
            updateActionStateSelect();
        });
    });

     var updateActionStateSelect = function() {
        // Here we are going to get the list of statuses to populate
        $("#existingActionStateNameSelect").empty();
        $("#existingActionStateNameSelect").append("<option value='None' selected='selected'>Choose an Action State...</option>");
        $.getJSON("/actionstates/", function(data) {
                $.each(data, function(key, value) {
                    $("#existingActionStateNameSelect").append("<option value='"+value.ActionStateID+"'>"+value.ActionStateName+"</option>");

                });
        });
    }

    var updateEditActionStateForm = function(state) {
        $("#existingActionStateName").val(state.ActionStateName);
        $("#existingActionStateFinished").prop('checked', state.ActionComplete);//  $('#input-1').val(status.ActionStateDescription);
        $("#existingActionStateDescription").val(state.ActionStateDescription);
    };

    $("#mainrow").on("change", "#existingActionStateNameSelect", function() {
        var selectedStatusID = $("#existingActionStateNameSelect").val();
        if (selectedStatusID == "None") {
            return;
        }
        var status = $.getJSON("/actionstates/"+selectedStatusID, function(response) {
            updateEditActionStateForm(response)
        });
    });

    $("#mainrow").on("click", "#submitChooseActionStateToEditBtn", function(event) {
        event.preventDefault();
        if ($("#existingActionStateNameSelect").val() == "None") {
            return;
        }
        var selectedActionStateID = $("#existingActionStateNameSelect").val();

        // Here we create a Model for the particular Status we want to edit. We retrieve the Status
        // from the server with a matching ID to the one in the drop down.
        // Even though the server side model doesn't have id, it has StatusID, we have to set an id
        // property on the client side model so that it knows to use PUT, not POST.
        ActionState.findOne({id: selectedActionStateID}, function(state) {
            state.attr("id", selectedActionStateID);
            // Change the fields...
            state.attr("ActionStateName", $("#existingActionStateName").val());
            state.attr("ActionStateDescription", $("#existingActionStateDescription").val());
            state.attr("ActionComplete", $("#existingActionStateFinished").prop('checked'));
            // Save to the server
            state.save(function(saved) {
                $("#editActionStateFormBody").prepend("<div id='editStatusSuccessAlert' class='alert alert-success'>Action State Updated!</div>");
                updateEditActionStateForm(saved);
                updateActionStateSelect();
            });

        });

    });

    $("#mainrow").on("click", "#deleteActionStateBtn", function(event) {
        event.preventDefault();

        if ($("#existingActionStateNameSelect").val() == "None") {
            return;
        }
        $("#editActionStateFormBody").prepend("<div id='deleteActionStateConfirmationAlert' class='alert alert-danger'>" +
            "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
            "<h4 id='confirmDeleteMsg'>Are you sure you want to delete that state?</h4>" +
            "<p><button id='confirmDeleteActionStateBtn' type='button' class='btn btn-danger'>Yes, delete</button>&nbsp&nbsp</div>");
    });

    $("#mainrow").on("click", "#confirmDeleteActionStateBtn", function(event) {
        var selectedActionStateID = $("#existingActionStateNameSelect").val();
        ActionState.findOne({id: selectedActionStateID}, function(state) {
            state.attr("id", selectedActionStateID);
            state.destroy(function() {
                    updateActionStateSelect();
                    $("#confirmDeleteMsg").html("State deleted!");
                    $("#confirmDeleteActionStateBtn").hide();
                    $("#existingActionStateName").val("");
                    $("#existingActionStateDescription").val("");
            });

        });
    });

    $("#mainrow").on("click", "#submitCreateNewActionStateBtn", function(event) {
        event.preventDefault();
        var newState = new ActionState({ActionStateName: $("#newActionStateNameInput").val(),
                                        ActionStateDescription: $("#newActionStateDescriptionInput").val(),
                                        ActionComplete: $("#newActionStateComplete").prop('checked')
                                       });
        newState.save(function(saved) {
            $("#addNewActionStateFormBody").prepend("<div id='addActionStateConfirmationAlert' class='alert alert-success'>" +
            "<h4>Action State added!</h4></div>");
            $("#addActionStateConfirmationAlert").fadeOut(8000);
            $("#newActionStateNameInput").val("");
            $("#newActionStateDescriptionInput").val("");
        });
    });

});