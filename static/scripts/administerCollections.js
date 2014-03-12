steal(function() {
    $("#mainrow").on("click", "#createNewCollectionFormLink", function(event) {
        /**
         * This function handles displaying the create new collection form
         */
        $("#administerCollectionsDiv").load("/addNewCollectionForm/", function() {

        });

    });
    $("#mainrow").on("click", "#editCollectionFormLink", function(event) {
        /**
         * This function handles displaying the create new collection form
         */
        $("#administerCollectionsDiv").load("/editCollectionForm/", function() {

        });

    });
});