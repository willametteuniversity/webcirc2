steal(function() {
    /**
     * This module contains functionality to deal with creating new equipment
     * entries on the server.
     */

    jQuery.noConflict();
    $("#mainrow").on("click", "#createInventoryItemBtn", function(event) {
        /**
         * This is called when the user wants to create a new Inventory item
         */
        $("#addNewEquipmentDiv").load("/addNewInventoryItemForm/", function() {
            // TODO: Look at doing this using the Model functionality. Maybe move this to a utility function?

            /** Begin section to populate the form **/
                // This pulls all the valid locations to populate the text box.
                // TODO: Look for an error response and display appropriately
            $.getJSON("/locations/", function(data) {
                $("#storageLocationSelect").empty();
                $.each(data, function(key, val) {
                    $("#storageLocationSelect").append($('<option value="'+val.LocationID+'">'+val.LocationDescription+'</option>'));
                });
            });

            // This pulls all the valid statuses to populate
            // TODO: Look for an error response and display something
            $.getJSON("/statuses/", function(data) {
                $("#statusSelect").empty();
                $.each(data, function(key, val) {
                    $("#statusSelect").append($('<option value="'+val.StatusID+'">'+val.StatusDescription+'</option>'));
                });
            });

            /** Begin autocomplete configuration section for the new Inventory Item form **/
            // This section handles setting up the Bloodhound stuff for autocomplete. We are using the
            // typeahead.js module.
            var brands = new Bloodhound({
                datumTokenizer: function(d) {
                    return Bloodhound.tokenizers.whitespace(d.BrandName);
                },
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                remote: '/autocomplete/?model=brand&term=%QUERY'
            });

            brands.initialize();
            $("#brandInput").typeahead(null, {
                name: 'brands',
                displayKey: 'BrandName',
                source: brands.ttAdapter()
            });

            var models = new Bloodhound({
                datumTokenizer: function(d) {
                    return Bloodhound.tokenizers.whitespace(d.ModelDesignation);
                },
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                remote: '/autocomplete/?model=model&term=%QUERY'
            });

            models.initialize();
            $("#modelInput").typeahead(null, {
                name: 'models',
                displayKey: 'ModelDesignation',
                source: models.ttAdapter()
            });

            var categories = new Bloodhound({
                datumTokenizer: function(d) {
                    return Bloodhound.tokenizers.whitespace(d.LabelName);
                },
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                remote: '/autocomplete/?model=category&term=%QUERY'
            });

            categories.initialize();
            $("#categoryInput").typeahead(null, {
                name: 'categories',
                displayKey: 'LabelName',
                source: categories.ttAdapter()
            });

            var collections = new Bloodhound({
                datumTokenizer: function(d) {
                    return Bloodhound.tokenizers.whitespace(d.LabelName);
                },
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                remote: '/autocomplete/?model=collection&term=%QUERY'
            });

            collections.initialize();
            $("#collectionInput").typeahead(null, {
                name: 'collections',
                displayKey: 'CollectionName',
                source: collections.ttAdapter()
            });
            /** End of Bloodhound configuration section **/
        });
    });

    $("#mainrow").on("click", "#submitCreateNewInventoryItemBtn", function(event) {
        /**
         * This function handles the submission of the create new Inventory Item form
         */
        event.preventDefault();
        // First lets hide any existing alerts so they don't grow uncontrolled
        $(".alert").hide();
        var fieldMissing = false;

        /** Begin section to check that all required input fields have something in them **/
        var brandName = $("#brandInput").val();
        if (brandName == "") {
            $("#addNewInventoryItemFormBody").prepend("<div id='addNewEquipmentBrandNotEnteredAlert' class='alert alert-danger'>" +
                "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                "<h4 id='brandNotEnteredMsg'>Please enter a Brand!</h4>");
            fieldMissing = true;
        }
        var modelName = $("#modelInput").val();
        if (modelName == "") {
            $("#addNewInventoryItemFormBody").prepend("<div id='addNewEquipmentModelNotEnteredAlert' class='alert alert-danger'>" +
                "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                "<h4 id='modelNotEnteredMsg'>Please enter a Model!</h4>");
            fieldMissing = true;
        }
        var categoryName = $("#categoryInput").val();
        if (modelName == "") {
            $("#addNewInventoryItemFormBody").prepend("<div id='addNewEquipmentCategoryNotEnteredAlert' class='alert alert-danger'>" +
                "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                "<h4 id='categoryNotEnteredMsg'>Please enter a Category!</h4>");
            fieldMissing = true;
        }
        var collectionName = $("#collectionInput").val();
        if (collectionName == "") {
            $("#addNewInventoryItemFormBody").prepend("<div id='addNewEquipmentCollectionNotEnteredAlert' class='alert alert-danger'>" +
                "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                "<h4 id='collectionNotEnteredMsg'>Please enter a Collection!</h4>");
            fieldMissing = true;
        }
        // If we had any missing fields, don't bother to execute the rest, just return
        if (fieldMissing == true) {
            return;
        }
        /** END **/
        /** Here we begin the asynchronous AJAX calls to validate and retrieve the associated models from
         * the server. We do this so we can extract things like the ID and then feed it back to the server
         * when we save it.
         */
        $.when(
                ItemBrand.findOne({BrandName:brandName}, function(success){}, function(error) {
                    $("#addNewInventoryItemFormBody").prepend("<div id='addNewEquipmentBrandNotExistAlert' class='alert alert-danger'>" +
                        "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                        "<h4 id='itemBrandNotExistMsg'>That is not valid brand!</h4>");
                }),

                ItemModel.findOne({ModelName:modelName}, function(success){}, function(error){
                    $("#addNewInventoryItemFormBody").prepend("<div id='addNewEquipmentModelNotExistAlert' class='alert alert-danger'>" +
                        "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                        "<h4 id='itemModelNotExistMsg'>That is not valid model!</h4>");
                }),

                Label.findOne({LabelName:categoryName}, function(success){}, function(error) {
                    $("#addNewInventoryItemFormBody").prepend("<div id='addNewEquipmentCategoryNotExistAlert' class='alert alert-danger'>" +
                        "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                        "<h4 id='confirmDeleteMsg'>That is not valid category!</h4>");
                }),

                Collection.findOne({CollectionName:collectionName}, function(success){}, function(error){
                    $("#addNewInventoryItemFormBody").prepend("<div id='addNewEquipmentCollectionNotExistAlert' class='alert alert-danger'>" +
                        "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                        "<h4 id='confirmDeleteMsg'>That is not valid collection!</h4>");
                }))
            // If all of them completed successfully, the done() function gets executed.
            // We use the error callbacks of findOne up above to tell the user about any invalid
            // fields. That is, any models we have no record of on the server.
            .done(function(brand, model, category, collection) {
                steal.dev.log("Creating new inventory item...");
                // Make a new client side inventory item
                var newInventoryItem = new InventoryItem({BrandID:brand.BrandID,
                    ModelID:model.ModelID,
                    Description:$("#descriptionInput").val(),
                    Notes:$("#notesInput").val(),
                    CategoryID:category.LabelID,
                    //TODO: Need a field for parent category?
                    StatusID:$("#statusSelect").val(),
                    StorageLocation:$("#storageLocationSelect").val(),

                    CollectionID:collection.CollectionID
                });
                steal.dev.log("Saving new item to server...");
                // Try and save it to the server
                newInventoryItem.save(function(success) {
                    steal.dev.log("New inventory item saved to server")
                }, function(error) {
                    steal.dev.warn("Error saving new inventory item!");
                });
            });
    });

    $("#mainrow").on("click", "#createNonInventoryItemBtn", function(event) {
        /**
         * This function handles displaying the form for creating a non-Inventory Item
         */
        $("#addNewEquipmentDiv").load("/addNewNonInventoryItemForm/", function() {

            /** Begin section to populate the form **/
                // This pulls all the valid locations to populate the text box.
                // TODO: Look for an error response and display appropriately
            $.getJSON("/locations/", function(data) {
                $("#nonInventoryItemStorageLocationSelect").empty();
                $.each(data, function(key, val) {
                    $("#nonInventoryItemStorageLocationSelect").append($('<option value="'+val.LocationID+'">'+val.LocationDescription+'</option>'));
                });
            });

            // This pulls all the valid statuses to populate
            // TODO: Look for an error response and display something
            $.getJSON("/statuses/", function(data) {
                $("#nonInventoryStatusSelect").empty();
                $.each(data, function(key, val) {
                    $("#nonInventoryStatusSelect").append($('<option value="'+val.StatusID+'">'+val.StatusDescription+'</option>'));
                });
            });

            /** Begin Bloodhound setup section for typeahead.js **/
            var categories = new Bloodhound({
                datumTokenizer: function(d) {
                    return Bloodhound.tokenizers.whitespace(d.LabelName);
                },
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                remote: '/autocomplete/?model=category&term=%QUERY'
            });
            categories.initialize();
            $("#nonInventoryItemCategoryInput").typeahead(null, {
                name: 'categories',
                displayKey: 'LabelName',
                source: categories.ttAdapter()
            });

            var collections = new Bloodhound({
                datumTokenizer: function(d) {
                    return Bloodhound.tokenizers.whitespace(d.LabelName);
                },
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                remote: '/autocomplete/?model=collection&term=%QUERY'
            });

            collections.initialize();
            $("#nonInventoryItemCollectionInput").typeahead(null, {
                name: 'collections',
                displayKey: 'CollectionName',
                source: collections.ttAdapter()
            });
            /** End Bloodhound configuration section **/
        });
    });

    $("#mainrow").on("click", "#submitCreateNewNonInventoryItemBtn", function(event) {
        /**
         * This function handles the submission of the create new non-Inventory Item form
         */
        event.preventDefault();
        // First lets hide any existing alerts so they don't grow uncontrolled
        $(".alert").hide();
        steal.dev.log("Beginning creation of new non-inventory item...");
        var fieldMissing = false;

        /** Begin section to check that all required input fields have something in them **/
        steal.dev.log("Checking that all required fields have been filled out...");
        var name = $("#nonInventoryItemNameInput").val();
        if (name == "") {
            $("#addNewNonInventoryItemFormBody").prepend("<div id='addNewEquipmentNameNotEnteredAlert' class='alert alert-danger'>" +
                "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                "<h4 id='brandNotEnteredMsg'>Please enter a name for your item!</h4>");
            fieldMissing = true;
        }

        var description = $("#nonInventoryItemDescriptionInput").val();
        if (description == "") {
            $("#addNewNonInventoryItemFormBody").prepend("<div id='addNewEquipmentDescriptionNotEnteredAlert' class='alert alert-danger'>" +
                "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                "<h4 id='descriptionNotEnteredMsg'>Please enter a description for your item!</h4>");
            fieldMissing = true;
        }

        var category = $("#nonInventoryItemCategoryInput").val();
        if (category == "") {
            $("#addNewNonInventoryItemFormBody").prepend("<div id='addNewEquipmentCategoryNotEnteredAlert' class='alert alert-danger'>" +
                "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                "<h4 id='categoryNotEnteredMsg'>Please enter a category for your item!</h4>");
            fieldMissing = true;
        }

        var quantity = $("#nonInventoryItemQuantityInput").val();
        if (quantity == "") {
            $("#addNewNonInventoryItemFormBody").prepend("<div id='addNewEquipmentQuantityNotEnteredAlert' class='alert alert-danger'>" +
                "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                "<h4 id='quantityNotEnteredMsg'>Please enter a quantity for your item!</h4>");
            fieldMissing = true;
        }

        var collection = $("#nonInventoryItemCollectionInput").val();
        if (collection == "") {
            $("#addNewNonInventoryItemFormBody").prepend("<div id='addNewEquipmentCollectionNotEnteredAlert' class='alert alert-danger'>" +
                "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                "<h4 id='collectionNotEnteredMsg'>Please enter a collection for your item!</h4>");
            fieldMissing = true;
        }

        if (fieldMissing == true) {
            steal.dev.warn("Field missing from form Add New Non-Inventory item, aborting");
            return;
        }
        steal.dev.log("Beginning retrievals for new Non-Inventory item");
        $.when(
                Label.findOne({LabelName:category}, function(success){
                    steal.dev.log("Found valid category for new non-inventory item");
                }, function(error) {
                    steal.dev.warn("Error retrieving category for new Non-Inventory Item");
                    $("#addNewNonInventoryItemFormBody").prepend("<div id='addNewEquipmentCategoryNotExistAlert' class='alert alert-danger'>" +
                        "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                        "<h4 id='categoryNotExistMsg'>That is not valid category!</h4>");
                }),
                Collection.findOne({CollectionName:collection}, function(success){
                    steal.dev.log("Found valid category for new non-inventory item");
                }, function(error) {
                    steal.dev.warn("Error retrieving collection for new Non-Inventory Item");
                    $("#addNewNonInventoryItemFormBody").prepend("<div id='addNewEquipmentCollectionNotExistAlert' class='alert alert-danger'>" +
                        "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                        "<h4 id='collectionNotExistMsg'>That is not valid collection!</h4>");
                }))
                .done(function(category, collection) {
                    steal.dev.log("Creating new non-inventory item client side");
                    var newNonInventoryItem = new NonInventoryItem({
                        Description:$("#nonInventoryItemDescriptionInput").val(),
                        Notes:$("#nonInventoryItemNote").val(),
                        CategoryID:category.LabelID,
                        StatusID:$("#nonInventoryStatusSelect").val(),
                        StorageLocation:$("#nonInventoryItemStorageLocationSelect").val(),
                        CollectionID:collection.CollectionID,
                        Quantity:$("#nonInventoryItemQuantityInput").val()
                    });
                    steal.dev.log("Saving new non inventory item to server...");
                    console.log(newNonInventoryItem);
                    newNonInventoryItem.save(function(success) {
                        steal.dev.log("Inventory item saved to server");
                    }, function(error) {
                        steal.dev.log("Failed to save new non-inventory item to server");
                    });
                    steal.dev.log("New non inventory item saved to server");
                });

    });

});