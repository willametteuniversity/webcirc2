steal(function() {

    $("#saveNewLabelBtn").on("click", function(event) {

        event.preventDefault();
        var newLabel = new Label({LabelName: $("#newLabelNameText").val()});
        newLabel.save(function(saved) {
            console.log("Label saved");
        })
        //var newLabelForm =
    })
})