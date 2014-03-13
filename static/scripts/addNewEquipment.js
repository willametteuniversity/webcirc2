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
            /** End of Bloodhound configuration section **/
        });
    });

    $("#mainrow").on("click", "#submitCreateNewInventoryItemBtn", function(event) {
        /**
         * This function handles the submission of the create new Inventory Item form
         */
        event.preventDefault();
        // Adding an inventory item is a teensy bit more complicated.
        // First, let's figure out if the Brand they entered already exists, or if we need to
        // create it.
        var brandName = $("#brandInput").val();
        console.log("Brand name is: "+brandName)
        var newItemBrand = ItemBrand.findOne({BrandName:brandName}, function(success) {
            // If it exists, 
        }, function(failure) {
            console.log("Brand does not exist!");
        });

    });
    $("#mainrow").on("click", "#createNonInventoryItemBtn", function(event) {
        /**
         * This function handles displaying the form for creating a non-Inventory Item
         */
        $("#addNewEquipmentDiv").load("/addNewNonInventoryItemForm/", function() {
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
            /** End Bloodhound configuration section **/
        });


    });

    $("#mainrow").on("click", "#submitCreateNewNonInventoryItemBtn", function(event) {
        /**
        * This function handles the submission of the create new non-Inventory Item form
        */


    });

});