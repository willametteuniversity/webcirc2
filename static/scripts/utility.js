var loadLabels = function () {
    /**
     * This function loads the currently existant labels into the box
     */

    Label.findAll({}, function (labels) {
        $("#labelListBox").empty();
        var numLabels = labels.length;
        for (x = 0; x < numLabels; x++) {
            $("#labelListBox").append("<option value=\"" + labels.attr(x).LabelID + "\">" + labels.attr(x).LabelName + "</option>");
        }
    });
};