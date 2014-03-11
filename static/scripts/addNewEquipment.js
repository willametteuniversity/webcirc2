steal(function() {
    jQuery.noConflict();
    $("#mainrow").on("click", "#createInventoryItemBtn", function(event) {
        $("#addNewEquipmentDiv").load("/addNewInventoryItemForm/", function() {
            // TODO: Look at doing this using the Model functionality. Maybe move this to a utility function?

            /** Begin section to populate the form **/
            // This pulls all the valid locations to populate the text box.
            $.getJSON("/locations/", function(data) {
                $("#storageLocationSelect").empty();
                $.each(data, function(key, val) {
                    $("#storageLocationSelect").append($('<option value="'+val.LocationID+'">'+val.LocationDescription+'</option>'));
                });
            });

            // This pulls all the valid statuses to populate
            $.getJSON("/statuses/", function(data) {
                $("#statusSelect").empty();
                $.each(data, function(key, val) {
                    $("#statusSelect").append($('<option value="'+val.StatusID+'">'+val.StatusDescription+'</option>'));
                });
            });

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
            /** End section to populate the form **/
        });
    });

    $("#mainrow").on("click", "#createNonInventoryItemBtn", function(event) {
        $("#addNewEquipmentDiv").load("/addNewNonInventoryItemForm/");
    });

});