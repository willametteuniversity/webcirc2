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
        $("#actionType").append("<option value=\"\" selected=\"\">Please select an Action Type...</option>");
        for (x = 0; x < numActionTypes; x++) {
            $("#actionType").append("<option value=\"" + actionTypes.attr(x).ActionTypeID + "\">" + actionTypes.attr(x).ActionTypeName + "</option>");
        }
    });
}

var loadOrigins = function() {
    Location.findAll({}, function (locations) {
        $("#actionOrigin").empty();
        $("#actionOrigin").append("<option value=\"\" selected=\"\">Please select an Origin...</option>");
        var numLocations = locations.length;
        // TODO: This should be done with $.each
        for (x = 0; x < numLocations; x++) {

            $("#actionOrigin").append("<option value=\"" + locations.attr(x).LocationID + "\">" + locations[x].LocationDescription + "</option>");
        }
    })
};

var loadDestinations = function() {
    Location.findAll({}, function (locations) {
        $("#actionDestination").empty();
        $("#actionDestination").append("<option value=\"\" selected=\"\">Please select a Destination...</option>");
        var numLocations = locations.length;
        for (x = 0; x < numLocations; x++) {

            $("#actionDestination").append("<option value=\"" + locations.attr(x).LocationID + "\">" + locations[x].LocationDescription + "</option>");
        }
    })
};

var loadAssignUserToAction = function() {
    User.findAll({}, function (users) {
       $("#actionAssignedUser").empty();
        $("#actionAssignedUser").append("<option value=\"\" selected=\"\">Please select User...</option>");
        $.each(users, function(index, value) {
            $("#actionAssignedUser").append("<option value=\"" + value.id+ "\">" + value.username+"</option>");
        })
    });
};

var loadTodaysActions = function () {
    var todayObj = new Date();
    var todayString = todayObj.getFullYear() + '-' + (todayObj.getMonth() + 1) + '-' + todayObj.getDate();

    var startRow = function(action){
        var row = "";
        row += '<tr><td>';
        row += '<button class="btn btn-default btn-small">';
        row += action.ActionID;
        row += '</button></td><td>';
        row += '<button class="btn btn-default btn-small">';
        row += action.Reservation[0];
        row += '</button></td><td class="middletext">';
        return row;
    };

    var getActionType = function(action) {
        return new Promise(function(resolve, reject) {
            ActionType.findOne({id: action.ActionTypeID}, function (actionType) {
                resolve(actionType.ActionTypeName);
            });
        });
    };

    var getLocationString = function(locationID) {
        return new Promise(function(resolve, reject) {
            Location.findOne({id: locationID}, function(location){
                Building.findOne({id: location.BuildingID}, function(building){
                    var locationString = building.BuildingCode + '-' + location.RoomNumber;
                    resolve(locationString);
                });
            });
        });
    };

    var getActionOperator = function(action) {
        return new Promise(function(resolve, reject) {
            User.findOne({id: action.AssignedOperatorID}, function (user) {
                resolve(user.username);
            });
        });
    };

    var formatDate = function(dateString) {
        return new Date(dateString).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    Action.findAll({
        //date: todayString
    }, function (actions) {
        $.each(actions, function(index, action) {
            var row = startRow(action);
            getActionType(action).then(function(actionType){
                row += actionType + '</td><td>';
                row += formatDate(action.StartTime) + '</td><td>';
                row += formatDate(action.EndTime) + '</td><td>';
                getLocationString(action.Origin).then(function(originString){
                    row += originString + '</td><td>';
                    getLocationString(action.Destination).then(function(destinationString){
                        row += destinationString + '</td><td>';
                        row += "equipment" + '</td><td>';
                        row += action.ActionNotes + '</td><td>';
                        getActionOperator(action).then(function(operator){
                            row += operator  + '</td>';
                            $('#todaysActionsTableBody').append(row);
                        });
                    });
                });
            });
        });
    });



    //Action.findAll({
    //    //date: todayString
    //}, function (actions) {
    //    $.each(actions, function(index, value) {
    //        ActionType.findOne({id: value.ActionTypeID}, function (actionType) {
    //            Location.findOne({id: value.Origin}, function (origin) {
    //                Location.findOne({id: value.Destination}, function(destination) {
    //                    User.findOne({id: value.AssignedOperatorID}, function(user) {
    //                        Building.findOne({id: origin.BuildingID}, function(origin_building) {
    //                            Building.findOne({id: destination.BuildingID}, function(destination_building) {
    //                                InventoryItem.findAll({action_id: value.ActionID}, function(equipment) {
    //                                    var equipment_ids = "";
    //                                    $.each(equipment, function(index, item){
    //                                                equipment_ids += "Item"//category;
    //                                                equipment_ids += " (";
    //                                                equipment_ids += item.ItemID;
    //                                                equipment_ids += ")";
    //                                                equipment_ids += ", ";
    //                                    });
    //                                    equipment_ids = equipment_ids.slice(0,equipment_ids.length-2)
    //                                    $('#todaysActionsTableBody').append(
    //                                        '<tr><td>' + value.ActionID + '</td><td>' +
    //                                        value.Reservation[0] + '</td><td>' +
    //                                        actionType.ActionTypeName + '</td><td>' +
    //                                        new Date(value.StartTime).toLocaleTimeString('en-US', {
    //                                            hour: '2-digit',
    //                                            minute: '2-digit'
    //                                        }) + '</td><td>' +
    //                                        new Date(value.EndTime).toLocaleTimeString('en-US', {
    //                                            hour: '2-digit',
    //                                            minute: '2-digit'
    //                                        }) + '</td><td>' +
    //                                        origin_building.BuildingCode + '-' + origin.RoomNumber + '</td><td>' +
    //                                        destination_building.BuildingCode + '-' + destination.RoomNumber + '</td><td>'+
    //                                        equipment_ids+'</td><td>'+
    //                                        value.ActionNotes + '</td><td>' +
    //                                        user.username + '</td></tr>'
    //                                    );
    //                                });
    //                            });
    //                        });
    //                    });
    //                });
    //            });
    //        });
    //    });
    //});

};