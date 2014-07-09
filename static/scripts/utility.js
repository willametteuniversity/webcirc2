var loadLabels = function () {
    /**
     * This function loads the currently existant labels into the box
     */
    Label.findAll({}, function (labels) {
        $("#labelListBox").empty();
        console.log(labels);
        //labels.comparator = "LabelName";
        //labels.sort();
        var numLabels = labels.length;
        for (x = 0; x < numLabels; x++) {
            $("#labelListBox").append("<option value=\"" + labels.attr(x).LabelID + "\">" + labels.attr(x).LabelName + "</option>");
        }
    });
};

var findBuildingByID = function(all_buildings, id) {
    for (var i=0 ; i < all_buildings.length ; i++) {
        if (all_buildings[i].BuildingID == id) {
            return all_buildings[i].BuildingName
        }
    }
}

var fillNewReservation = function () {
    Building.findAll({}, function(all_buildings) {
        Location.findAll({}, function (locations) {
            $("#actionOrigin").empty();
            var count = locations.length;
            for (x = 0; x < count; x++) {
                buildingName = findBuildingByID(all_buildings, locations.attr(x).BuildingID);
                $("#actionOrigin").append("<option value=\"" + locations.attr(x).LocationID + "\">" + buildingName + " " + locations.attr(x).RoomNumber + "</option>");
                $("#actionDestination").append("<option value=\"" + locations.attr(x).LocationID + "\">" + buildingName + " " + locations.attr(x).RoomNumber + "</option>");
            }
        });
    });
    ActionType.findAll({}, function(actions) {
        var count = actions.length;
        for (x = 0; x < count; x++) {
            $("#actionType").append("<option value=\"" + actions.attr(x).ActionTypeID + "\">" + actions.attr(x).ActionTypeName + "</option>");
        }
    });
};