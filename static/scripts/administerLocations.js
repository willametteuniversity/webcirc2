steal(function() {
    $("#mainrow").on("click", "#createNewLocationFormLink", function(event) {
        /**
         * Load the new new location form
         */
        $("#administerLocationsDiv").load("/addNewLocationForm/", function() {
        });
    });

    $("#mainrow").on("click", "#chooseLocationToEditLink", function(event) {
        /**
         * Load the edit new location window
         */
        $("#administerLocationsDiv").load("/chooseLocationToEditForm/", function() {
            updateLocationSelect();
        });
    });

    var updateLocationSelect = function() {
        // Here we are going to get the list of Locations to populate
        $("#existingLocationNameSelect").empty();
        $("#existingLocationNameSelect").append("<option value='None' selected='selected'>Choose a Location...</option>");
        $.getJSON("/locations/", function(data) {
                // This populates the dropdown to let people choose a Location to edit
                $.each(data, function(key, value) {
                    // If we had one selected prior, remember to restore that one as the selected one
                    $("#existingLocationNameSelect").append("<option value='"+value.LocationID+"'>"+value.LocationName+"</option>");
                });
        });
    }

    var updateEditLocationForm = function(location) {
        $("#existingLocationName").val(Location.LocationName);
        $("#existingLocationDescription").val(Location.LocationDescription);
    };

    $("#mainrow").on("change", "#existingLocationNameSelect", function() {
        /**
         * This function handles form pre-population when they choose a Location from
         * the drop down.
         */
        var selectedLocationID = $("#existingLocationNameSelect").val();
        // This is to handle them choosing the "Choose a Location..." option in the dropdown
        if (selectedLocationID == "None") {
            return;
        }
        // When they choose an existing Location from the dropdown, we want to pre-populate the form
        // with existing values
        var Location = $.getJSON("/Locations/"+selectedLocationID, function(response) {
            updateEditLocationForm(response)
        });
    });

    $("#mainrow").on("click", "#submitChooseLocationToEditBtn", function(event) {
        event.preventDefault();
        var selectedLocationID = $("#existingLocationNameSelect").val();

        // Here we create a Model for the particular Location we want to edit. We retrieve the Location
        // from the server with a matching ID to the one in the drop down.
        // Even though the server side model doesn't have id, it has LocationID, we have to set an id
        // property on the client side model so that it knows to use PUT, not POST.
        Location.findOne({id: selectedLocationID}, function(Location) {
            Location.attr("id", selectedLocationID);
            // Change the fields...
            Location.attr("LocationName", $("#existingLocationName").val());
            Location.attr("LocationDescription", $("#existingLocationDescription").val());
            // Save to the server
            Location.save(function(saved) {
                updateEditLocationForm(saved);
                updateLocationSelect();
                $("#editLocationFormBody").prepend("<div id='editLocationSuccessAlert' class='alert alert-success'>" +
                "<h4>Location Edited!</h4></div>");
                $("#editLocationSuccessAlert").fadeOut(8000);
            });

        });

    });

    $("#mainrow").on("click", "#deleteLocationBtn", function(event) {
        /**
         * This function handles the pressing of the Delete button when someone wants to delete
         * a Location. It will show a confirmation alert.
         */
        event.preventDefault();

        if ($("#existingLocationNameSelect").val() == "None") {
            return;
        }
        $("#editLocationFormBody").prepend("<div id='deleteLocationConfirmationAlert' class='alert alert-danger'>" +
            "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
            "<h4 id='confirmDeleteMsg'>Are you sure you want to delete that Location?</h4>" +
            "<p><button id='confirmDeleteLocationBtn' type='button' class='btn btn-danger'>Yes, delete</button>&nbsp&nbsp</div>");
    });

    $("#mainrow").on("click", "#confirmDeleteLocationBtn", function(event) {
        /**
         * This function handles the pressing of the confirm deletion button. It actually deletes the
         * object from the server.
         */
        var selectedLocationID = $("#existingLocationNameSelect").val();
        Location.findOne({id: selectedLocationID}, function(Location) {
            Location.attr("id", selectedLocationID);
            Location.destroy(function() {
                            updateLocationSelect();
                            $("#confirmDeleteMsg").html("Location deleted!");
                            $("#confirmDeleteLocationBtn").hide();
                            $("#existingLocationName").val("");
                            $("#existingLocationDescription").val("");
            });
        });
    });

    $("#mainrow").on("click", "#submitCreateNewLocationBtn", function(event) {
        /**
         * This function handles the pressing of the create new Location button
         */
        event.preventDefault();
        var newLocation = new Location({
                            BuildingID: 1,
                            RoomNumber: $("#newLocationRoomNumberInput").val(),
                            LocationDescription: $("#newLocationDescriptionInput").val()
                            });
        newLocation.save(function(saved) {
            $("#addNewLocationFormBody").prepend("<div id='addLocationConfirmationAlert' class='alert alert-success'>" +
            "<h4>Location added!</h4></div>");
            $("#addLocationConfirmationAlert").fadeOut(8000);
            $("#newLocationNameInput").val("");
            $("#newLocationDescriptionInput").val("");
        });
    });
});