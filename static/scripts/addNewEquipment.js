steal(function() {

    $("#mainrow").on("click", "#createInventoryItemBtn", function(event) {
        $("#addNewEquipmentDiv").load("/addNewInventoryItemForm");
    });

    $("#mainrow").on("click", "#createNonInventoryItemBtn", function(event) {
        $("#addNewEquipmentDiv").load("/addNewNonInventoryItemForm");
    });

});