steal(function() {

    $("#saveNewLabelBtn").on("click", function(event) {
        event.preventDefault();
        var newLabel = new Label({LabelName: $("#newLabelNameText").val()});
        newLabel.save(function(saved) {
            $("#closeAddNewLabelModalBtn").click();
            loadLabels();
        });
    });

    $("#mainrow").on("click", "#delLabelBtn", function(event) {
        event.preventDefault();
        var labelToDelete = $("#labelListBox").val();
        for (x = 0; x < labelToDelete.length; x++) {
            Label.destroy(labelToDelete[x]).then(function() {
                loadLabels();
            });
        }
    });
});