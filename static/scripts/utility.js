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
    /**
     * This function searches for a building by ID in a list of buildings
     */
    // TODO: Do this even need to exist?
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
    /**
     * This function loads all the ActionTypes from the server
     */
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
    /**
     * This function loads all the Origins from the server
     */
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
    /**
     * This function loads all the Destinations from the server
     */
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

var loadTodaysActions = function (tarDate) {
    $('#todaysActionsTableBody').empty();
    if (tarDate) {
        var todayObj = tarDate;
    } else {
        var todayObj = new Date();
    }

    var todayString = todayObj.getFullYear() + '-' + (todayObj.getMonth() + 1) + '-' + todayObj.getDate();

    var getActionType = function(action) {
        return new Promise(function(resolve, reject) {
            return ActionType.findOne({id: action.ActionTypeID}, function (actionType) {
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

    var getActionCustomer = function(action) {
        return new Promise(function(resolve, reject) {
            Reservation.findOne({id: action.Reservation[0]}, function(reservation) {
                User.findOne({id: reservation.CustomerID}, function (user) {
                    resolve(user.username);
                });
            });
        });
    };

    var getItemCategoryName = function(item) {
        return Label.findOne({id: item.CategoryID}, function (category) {
            return category.LabelName;
        });
    };

    var getActionStates = function(action) {
        return new Promise(function(resolve, reject) {
            ActionState.findOne({id: action.ActionState}, function(currentState){
                //ActionState.findAll(function(possibleStates){                     // unexpected behavior in findAll
                $.getJSON( "/actionstates/", function( possibleStates ) {
                    var dropdown = '<div class="dropdown"><button class="btn btn-default btn-sm dropdown-toggle" type="button" data-toggle="dropdown" aria-expanded="true">';
                    dropdown += currentState.ActionStateName
                    dropdown += '<span class="caret"></span></button><ul class="dropdown-menu" role="menu">';
                    $.each(possibleStates, function (index, state) {
                        if (state.ActionStateID != action.ActionState) {
                            dropdown += '<li role="presentation"><a class="actionstate" action="';
                            dropdown += action.ActionID;
                            dropdown += '" state="';
                            dropdown += state.ActionStateID;
                            dropdown += '" role="menuitem" href="#">';
                            dropdown += state.ActionStateName;
                            dropdown += '</a></li>';
                        }
                    });
                    dropdown += '</ul></div>';
                    resolve(dropdown);
                });
            });
        });
    };

    var getItems = function(action, itemType, labelClass) {
        return new Promise(function (resolve, reject) {
            itemType.findAll({action_id: action.ActionID}, function (invItems) {
                if (invItems.length == 0) {
                    resolve(['', 0])
                }
                var actionCount = invItems.length;
                var argh = '';
                var total = 0;
                $.each(invItems, function (index, invItem) {
                    if (itemType != InventoryItem) {
                        argh += '<li class="' + labelClass + '"><span class="black">' + invItem.Description + ' (' + invItem.ItemID + ')' + '</span></li>';
                        actionCount -= 1;
                        total += 1;
                        if (actionCount == 0) {
                            resolve([argh, total]);
                        }
                    } else {
                        Label.findOne({id: invItem.CategoryID}, function(category) {
                            argh += '<li class="' + labelClass + '"><span class="black">' + category.LabelName + ' (' + invItem.ItemID + ')' + '</span></li>';
                            actionCount -= 1;
                            total += 1;
                            if (actionCount == 0) {
                                resolve([argh, total])
                            }
                        })
                    }

                });
            }, function(failed) {
                resolve([null, 0]);
            });
        });
    };

    var getEquipmentList = function(action) {
        return new Promise(function (resolve, reject) {
            var invItemsArr = [];
            var nonInvItemsArr = [];
            var consumableItemsArr = [];
            var c = 3;
            var doneGetItems = function () {
                var count = 0;
                if (invItemsArr[0] != null) {
                    var invItems = invItemsArr[0];
                    count += invItemsArr[1];
                }
                if (nonInvItemsArr[0] != null) {
                    var nonInvItems = nonInvItemsArr[0];
                    count += nonInvItemsArr[1];
                }
                if (consumableItemsArr[0] != null) {
                    var consumableItems = consumableItemsArr[0];
                    count += consumableItemsArr[1];
                }
                var word = 'item';
                if (count > 1) {
                    word += 's'
                };
                var eq = '<span class="header">Click to <span replace-text="hide">view</span> ' +  count + ' ' + word +'</span><br /><div class="collapse"><ul>';
                if (invItemsArr[0] != null) {
                    eq += invItems;
                }
                if (nonInvItemsArr[0] != null) {
                    eq += nonInvItems;
                }
                if (consumableItemsArr[0] != null) {
                    eq += consumableItems;
                }
                eq += '</ul></div>';
                resolve(eq);
            };
            getItems(action, InventoryItem, 'invlabel').then(function (result) {
                c -= 1;
                invItemsArr = result;
                if (c == 0) {
                    doneGetItems();
                }
            });

            getItems(action, NonInventoryItem, 'noninvlabel').then(function (result) {
                c -= 1;
                nonInvItemsArr = result;
                if (c == 0) {
                    doneGetItems();
                }
            });

            getItems(action, ConsumableItem, 'consumablelabel').then(function (result) {
                c -= 1;
                consumableItemsArr = result;
                if (c == 0) {
                    doneGetItems();
                }
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
        date: todayString
    }, function (actions) {
        $.each(actions, function(index, action) {
            var rowAttributes = {};
            var attributeCount = 7;
            var row = '<tr><td class="middletext">';
            var buildFinalRow = function() {
                row += formatDate(action.EndTime) + '</td><td class="middletext">';
                row += formatDate(action.StartTime) + '</td><td class="middletext">';
                row += '<button id="actionDetailModalButton" class="btn btn-default btn-xs" data-toggle="modal">';
                row += '<span id="' + action.ActionID + '" reservation="' + action.Reservation[0] + '">';
                row += rowAttributes['actionType'] + '</span></button></td><td class="middletext">';
                row += rowAttributes['originString'] + '</td><td class="middletext">';
                row += rowAttributes['destinationString'] + '</td><td class="middletext">';
                row += rowAttributes['equipmentList'] + '</td><td class="middletext">';
                row += '<button class="btn btn-default btn-xs">' + rowAttributes['customer']  + '</button></td><td class="middletext">';
                row += '' + rowAttributes['operator']  + '</td><td class="middletext">';
                if (action.ActionNotes == "") {
                    row += '</td><td class="middletext">';
                } else {
                    row += '<button class="btn btn-default btn-xs">view</button></td><td class="middletext">'
                }
                row += rowAttributes['stateOptions'] + '</td></tr>';//'done button</td>';                  // need to create a drop down that is set to current state
                $('#todaysActionsTableBody').append(row);
            };
            getActionType(action).then(function(actionType) {
                attributeCount -= 1;
                rowAttributes['actionType'] = actionType
                if (attributeCount == 0) {
                    buildFinalRow();
                }
            });

            getLocationString(action.Origin).then(function(originString) {
                attributeCount -= 1;
                rowAttributes['originString'] = originString;
                if (attributeCount == 0) {
                    buildFinalRow();
                }
            });

            getLocationString(action.Destination).then(function(destinationString){
                attributeCount -= 1;
                rowAttributes['destinationString'] = destinationString;
                if (attributeCount == 0) {
                    buildFinalRow();
                }
            });

            getEquipmentList(action).then(function(equipmentList) {
                attributeCount -= 1;
                rowAttributes['equipmentList'] = equipmentList;
                if (attributeCount == 0) {
                    buildFinalRow();
                }
            });

            getActionOperator(action).then(function(operator){
                attributeCount -= 1;
                rowAttributes['operator'] = operator;
                if (attributeCount == 0) {
                    buildFinalRow();
                }
            });

            getActionCustomer(action).then(function(customer){
                attributeCount -= 1;
                rowAttributes['customer'] = customer;
                if (attributeCount == 0) {
                    buildFinalRow();
                }
            });

            getActionStates(action).then(function(states){
                attributeCount -= 1;
                rowAttributes['stateOptions'] = states;
                if (attributeCount == 0) {
                    buildFinalRow();
                }
            });
        });
    }, function (errors) {
        console.log(errors);
    });
};