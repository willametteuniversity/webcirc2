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

var loadActionTypes = function() {
    ActionType.findAll({}, function (actionTypes) {
        $("#actionType").empty();
        var numActionTypes = actionTypes.length;
        for (x = 0; x < numActionTypes; x++) {
            $("#actionType").append("<option value=\"" + actionTypes.attr(x).ActionTypeID + "\">" + actionTypes.attr(x).ActionTypeName + "</option>");
        }
    });
}

var loadOrigins = function() {
    Location.findAll({}, function (locations) {
        $("#actionOrigin").empty();
        var numLocations = locations.length;
        for (x = 0; x < numLocations; x++) {

            $("#actionOrigin").append("<option value=\"" + locations.attr(x).LocationID + "\">" + locations[x].LocationDescription + "</option>");
        }
    })
};

var loadDestinations = function() {
    Location.findAll({}, function (locations) {
        $("#actionDestination").empty();
        var numLocations = locations.length;
        for (x = 0; x < numLocations; x++) {

            $("#actionDestination").append("<option value=\"" + locations.attr(x).LocationID + "\">" + locations[x].LocationDescription + "</option>");
        }
    })
};

var loadAssignUserToAction = function() {
    User.findAll({}, function (users) {
       $("#actionAssignedUser").empty();
        $.each(users, function(index, value) {
            $("#actionAssignedUser").append("<option value=\"" + value.id+ "\">" + value.username+"</option>");
        })
    });
};

var loadTodaysActions = function() {
    var todayObj = new Date();

    var todayString = todayObj.getFullYear()+'-'+(todayObj.getMonth()+1)+'-'+todayObj.getDate()
    Action.findAll({
        date: todayString
    }, function(actions) {
        steal.dev.log(actions);
    });

};