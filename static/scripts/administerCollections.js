steal(function() {
    $("#mainrow").on("click", "#createNewCollectionFormLink", function(event) {
        /**
         * This function handles displaying the create new collection form
         */
        $("#administerCollectionsDiv").load("/addNewCollectionForm/", function() {

        });

    });
    $("#mainrow").on("click", "#chooseCollectionToEditLink", function(event) {
        /**
         * This function handles displaying the edit new collection form
         */
        $("#administerCollectionsDiv").load("/chooseCollectionToEditForm/", function() {
            updateCollectionSelect();


        });
    });

    var updateCollectionSelect = function() {
        // Here we are going to get the list of collections to populate
        $("#existingCollectionNameSelect").empty();
        $("#existingCollectionNameSelect").append("<option value='None' selected='selected'>Choose a Collection...</option>");
        $.getJSON("/collections/", function(data) {

                // This populates the dropdown to let people choose a collection to edit
                $.each(data, function(key, value) {
                    // If we had one selected prior, remember to restore that one as the selected one
                    $("#existingCollectionNameSelect").append("<option value='"+value.CollectionID+"'>"+value.CollectionName+"</option>");

                });
        });
    }

    var updateEditCollectionForm = function(collection) {
        $("#existingCollectionName").val(collection.CollectionName);
        $("#existingCollectionDescription").val(collection.CollectionDescription);
    };

    $("#mainrow").on("change", "#existingCollectionNameSelect", function() {
        /**
         * This function handles form pre-population when they choose a collection from
         * the drop down.
         */
        var selectedCollectionID = $("#existingCollectionNameSelect").val();
        // This is to handle them choosing the "Choose a Collection..." option in the dropdown
        if (selectedCollectionID == "None") {
            return;
        }
        // When they choose an existing collection from the dropdown, we want to pre-populate the form
        // with existing values
        var collection = $.getJSON("/collections/"+selectedCollectionID, function(response) {
            updateEditCollectionForm(response)
        });
    });

    $("#mainrow").on("click", "#submitChooseCollectionToEditBtn", function(event) {
        event.preventDefault();
        var selectedCollectionID = $("#existingCollectionNameSelect").val();

        // Here we create a Model for the particular Collection we want to edit. We retrieve the Collection
        // from the server with a matching ID to the one in the drop down.
        // Even though the server side model doesn't have id, it has CollectionID, we have to set an id
        // property on the client side model so that it knows to use PUT, not POST.
        Collection.findOne({id: selectedCollectionID}, function(collection) {
            collection.attr("id", selectedCollectionID);
            // Change the fields...
            collection.attr("CollectionName", $("#existingCollectionName").val());
            collection.attr("CollectionDescription", $("#existingCollectionDescription").val());
            // Save to the server
            collection.save(function(saved) {
                $("#editCollectionFormBody").prepend("<div id='editCollectionSuccessAlert' class='alert alert-success'>Collection Updated!</div>");
                updateEditCollectionForm(saved);
                updateCollectionSelect();
            });

        });

    });

    $("#mainrow").on("click", "#deleteCollectionBtn", function(event) {
        /**
         * This function handles the pressing of the Delete button when someone wants to delete
         * a collection. It will show a confirmation alert.
         */
        event.preventDefault();

        if ($("#existingCollectionNameSelect").val() == "None") {
            return;
        }
        $("#editCollectionFormBody").prepend("<div id='deleteCollectionConfirmationAlert' class='alert alert-danger'>" +
            "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
            "<h4 id='confirmDeleteMsg'>Are you sure you want to delete that collection?</h4>" +
            "<p><button id='confirmDeleteCollectionBtn' type='button' class='btn btn-danger'>Yes, delete</button>&nbsp&nbsp</div>");
    });

    $("#mainrow").on("click", "#confirmDeleteCollectionBtn", function(event) {
        /**
         * This function handles the pressing of the confirm deletion button. It actually deletes the
         * object from the server.
         */
        var selectedCollectionID = $("#existingCollectionNameSelect").val();
        Collection.findOne({id: selectedCollectionID}, function(collection) {
            collection.attr("id", selectedCollectionID);
            collection.destroy(function() {
                            updateCollectionSelect();
                            $("#confirmDeleteMsg").html("Collection deleted!");
                            $("#confirmDeleteCollectionBtn").hide();
                            $("#existingCollectionName").val("");
                            $("#existingCollectionDescription").val("");
            });

        });
    });
    
    $("#mainrow").on("click", "#submitCreateNewCollectionBtn", function(event) {
        /**
         * This function handles the pressing of the create new collection button
         */
            event.preventDefault();
        var newCollection = new Collection({CollectionName: $("#newCollectionNameInput").val(),
                            CollectionDescription: $("#newCollectionDescriptionInput").val()
                            });
        newCollection.save(function(saved) {
            $("#addNewCollectionFormBody").prepend("<div id='addCollectionConfirmationAlert' class='alert alert-success'>" +
            "<h4>Collection added!</h4></div>");
            $("#addCollectionConfirmationAlert").fadeOut(8000);
            $("#newCollectionNameInput").val("");
            $("#newCollectionDescriptionInput").val("");
        });
    });
});