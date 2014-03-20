steal(function() {
    $("#mainrow").on("click", "#createNewBuildingFormLink", function(event) {
        /**
         * This function handles displaying the create new Building form
         */
        $("#administerBuildingsDiv").load("/addNewBuildingForm/", function() {

        });

    });
    $("#mainrow").on("click", "#chooseBuildingToEditLink", function(event) {
        /**
         * This function handles displaying the edit new Building form
         */
        $("#administerBuildingsDiv").load("/chooseBuildingToEditForm/", function() {
            updateBuildingSelect();


        });
    });

    var updateBuildingSelect = function() {
        // Here we are going to get the list of Buildings to populate
        $("#existingBuildingNameSelect").empty();
        $("#existingBuildingNameSelect").append("<option value='None' selected='selected'>Choose a Building...</option>");
        $.getJSON("/buildings/", function(data) {

                // This populates the dropdown to let people choose a Building to edit
                $.each(data, function(key, value) {
                    // If we had one selected prior, remember to restore that one as the selected one
                    $("#existingBuildingNameSelect").append("<option value='"+value.BuildingID+"'>"+value.BuildingName+"</option>");

                });
        });
    }

    var updateEditBuildingForm = function(Building) {
        $("#existingBuildingName").val(Building.BuildingName);
        $("#existingBuildingCode").val(Building.BuildingCode);
    };

    $("#mainrow").on("change", "#existingBuildingNameSelect", function() {
        /**
         * This function handles form pre-population when they choose a Building from
         * the drop down.
         */
        var selectedBuildingID = $("#existingBuildingNameSelect").val();
        // This is to handle them choosing the "Choose a Building..." option in the dropdown
        if (selectedBuildingID == "None") {
            return;
        }
        // When they choose an existing Building from the dropdown, we want to pre-populate the form
        // with existing values
        var Building = $.getJSON("/buildings/"+selectedBuildingID, function(response) {
            updateEditBuildingForm(response)
        });
    });

    $("#mainrow").on("click", "#submitChooseBuildingToEditBtn", function(event) {
        event.preventDefault();
        var selectedBuildingID = $("#existingBuildingNameSelect").val();

        // Here we create a Model for the particular Building we want to edit. We retrieve the Building
        // from the server with a matching ID to the one in the drop down.
        // Even though the server side model doesn't have id, it has BuildingID, we have to set an id
        // property on the client side model so that it knows to use PUT, not POST.
        Building.findOne({id: selectedBuildingID}, function(Building) {
            Building.attr("id", selectedBuildingID);
            // Change the fields...
            Building.attr("BuildingName", $("#existingBuildingName").val());
            Building.attr("BuildingCode", $("#existingBuildingCode").val());
            // Save to the server
            Building.save(function(saved) {
                $("#editBuildingFormBody").prepend("<div id='editBuildingSuccessAlert' class='alert alert-success'>Building Updated!</div>");
                updateEditBuildingForm(saved);
                updateBuildingSelect();
            });

        });

    });

    $("#mainrow").on("click", "#deleteBuildingBtn", function(event) {
        /**
         * This function handles the pressing of the Delete button when someone wants to delete
         * a Building. It will show a confirmation alert.
         */
        event.preventDefault();

        if ($("#existingBuildingNameSelect").val() == "None") {
            return;
        }
        $("#editBuildingFormBody").prepend("<div id='deleteBuildingConfirmationAlert' class='alert alert-danger'>" +
            "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
            "<h4 id='confirmDeleteMsg'>Are you sure you want to delete that Building?</h4>" +
            "<p><button id='confirmDeleteBuildingBtn' type='button' class='btn btn-danger'>Yes, delete</button>&nbsp&nbsp</div>");
    });

    $("#mainrow").on("click", "#confirmDeleteBuildingBtn", function(event) {
        /**
         * This function handles the pressing of the confirm deletion button. It actually deletes the
         * object from the server.
         */
        var selectedBuildingID = $("#existingBuildingNameSelect").val();
        Building.findOne({id: selectedBuildingID}, function(Building) {
            Building.attr("id", selectedBuildingID);
            Building.destroy(function() {
                            updateBuildingSelect();
                            $("#confirmDeleteMsg").html("Building deleted!");
                            $("#confirmDeleteBuildingBtn").hide();
                            $("#existingBuildingName").val("");
                            $("#existingBuildingCode").val("");
            });

        });
    });
    
    $("#mainrow").on("click", "#submitCreateNewBuildingBtn", function(event) {
        /**
         * This function handles the pressing of the create new Building button
         */
            event.preventDefault();
        var newBuilding = new Building({BuildingName: $("#newBuildingNameInput").val(),
                            BuildingCode: $("#newBuildingCodeInput").val()
                            });
        newBuilding.save(function(saved) {
            $("#addNewBuildingFormBody").prepend("<div id='addBuildingConfirmationAlert' class='alert alert-success'>" +
            "<h4>Building added!</h4></div>");
            $("#addBuildingConfirmationAlert").fadeOut(8000);
            $("#newBuildingNameInput").val("");
            $("#newBuildingCodeInput").val("");
        });
    });
});