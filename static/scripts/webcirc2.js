$(document).ready(function() {
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    steal("can/can.js", function() {});
    steal("scripts/utility.js", function() {});
    steal("scripts/models/action.js", function() {});
    steal("scripts/models/actionType.js", function() {});
    steal("scripts/models/building.js", function() {});
    steal("scripts/models/collection.js", function() {});
    steal("scripts/models/label.js", function() {});
    steal("scripts/models/location.js", function() {});
    steal("scripts/models/itemBrand.js", function() {});
    steal("scripts/models/itemModel.js", function() {});
    steal("scripts/models/consumableItem.js", function() {});
    steal("scripts/models/inventoryItem.js", function() {});
    steal("scripts/models/nonInventoryItem.js", function() {});
    steal("scripts/models/user.js", function() {});
    steal("scripts/models/status.js", function() {});
    steal("scripts/models/reservation.js", function() {});
    steal("jstree/dist/jstree.min.js", function() {});
    steal("scripts/labelAndCategoryMgmt.js", function() {
        $.ajaxPrefilter(function(options, originalOptions, jqXHR) {
            /**
             * This function handles inserting out CSRF token into outgoing
             * AJAX requests
             */
            if ( options.processData
            && /^application\/json((\+|;).+)?$/i.test( options.contentType )
            && /^(post|put|delete)$/i.test( options.type )
            ) {
                options.data = JSON.stringify( originalOptions.data );
            }
            if (!options.crossDomain) {
                if (csrftoken) {
                    return jqXHR.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });
    });
    steal("scripts/addNewEquipment.js", function() {});
    steal("scripts/addNewReservation.js", function() {});
    steal("scripts/viewTodaysActions.js", function() {});
    steal("scripts/administerCollections.js", function() {
        $.ajaxPrefilter(function(options, originalOptions, jqXHR) {
            /**
             * This function handles inserting out CSRF token into outgoing
             * AJAX requests
             */
            if ( options.processData
            && /^application\/json((\+|;).+)?$/i.test( options.contentType )
            && /^(post|put|delete)$/i.test( options.type )
            ) {
                options.data = JSON.stringify( originalOptions.data );
            }
            if (!options.crossDomain) {
                if (csrftoken) {
                    return jqXHR.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });
    });
    steal("scripts/administerLocations.js", function() {
        $.ajaxPrefilter(function(options, originalOptions, jqXHR) {
            /**
             * This function handles inserting out CSRF token into outgoing
             * AJAX requests
             */
            if ( options.processData
            && /^application\/json((\+|;).+)?$/i.test( options.contentType )
            && /^(post|put|delete)$/i.test( options.type )
            ) {
                options.data = JSON.stringify( originalOptions.data );
            }
            if (!options.crossDomain) {
                if (csrftoken) {
                    return jqXHR.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });
    });
    steal("scripts/administerBuildings.js", function() {
        $.ajaxPrefilter(function(options, originalOptions, jqXHR) {
            /**
             * This function handles inserting out CSRF token into outgoing
             * AJAX requests
             */
            if ( options.processData
            && /^application\/json((\+|;).+)?$/i.test( options.contentType )
            && /^(post|put|delete)$/i.test( options.type )
            ) {
                options.data = JSON.stringify( originalOptions.data );
            }
            if (!options.crossDomain) {
                if (csrftoken) {
                    return jqXHR.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });
    });
    steal("scripts/administerActionTypes.js", function() {
        $.ajaxPrefilter(function(options, originalOptions, jqXHR) {
            /**
             * This function handles inserting out CSRF token into outgoing
             * AJAX requests
             */
            if ( options.processData
            && /^application\/json((\+|;).+)?$/i.test( options.contentType )
            && /^(post|put|delete)$/i.test( options.type )
            ) {
                options.data = JSON.stringify( originalOptions.data );
            }
            if (!options.crossDomain) {
                if (csrftoken) {
                    return jqXHR.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });
    });

    steal("scripts/administerStatuses.js", function() {
        $.ajaxPrefilter(function(options, originalOptions, jqXHR) {
            /**
             * This function handles inserting out CSRF token into outgoing
             * AJAX requests
             */
            if ( options.processData
            && /^application\/json((\+|;).+)?$/i.test( options.contentType )
            && /^(post|put|delete)$/i.test( options.type )
            ) {
                options.data = JSON.stringify( originalOptions.data );
            }
            if (!options.crossDomain) {
                if (csrftoken) {
                    return jqXHR.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });
    });
    $("#registerBtn").on("click", function(event) {
        /**
         * This function handles the register button being clicked on the main page.
         */
       $("#mainrow").load("/registerNewUser/");
    });

    $("#signInBtn").on("click", function(event) {
        /**
         * This function handles a user wanting to sign in
         */
        event.preventDefault();
        var loginForm = $("#signInForm").serialize();
        $.post("/login/", loginForm, function(response){
            location.reload();
        });
    });
    $("#registerBtn").on("click", function(event) {
        /**
         * This function handles the register button being clicked on the main page.
         */
       $("#mainrow").load("/registerNewUser/");
    });


    $("#signInBtn").on("click", function(event) {
        /**
         * This function handles a user wanting to sign in
         */
        event.preventDefault();
        var loginForm = $("#signInForm").serialize();
        $.post("/login/", loginForm, function(response){
            location.reload();
        });
    });

    $("#labelAndCategoryMgmtLink").on("click", function(event) {
        /**
         * This function handles the Label and Category Mgmt link being clicked.
         */
         $("#mainrow").load("/labelAndCategoryMgmt/", function() {
             loadLabels();
             $("#categoryMasterTree").jstree({
                 'core' : {
                    'data' : {
                        'url' : '/categoryHierarchy/'
                     },
                     'check_callback' : true

                 },
                 'plugins' : ['dnd']
             });
             $("#categoryMasterTree").on("move_node.jstree", function (e, data) {
                 $.ajax({
                     url:'/labels/'+data.node.id,
                     type: 'PUT',
                     data: {
                         ParentCategory:data.parent,
                         LabelName:data.node.text
                     }
                 });
             });
         });
    });

    $("#statusAdministrationLink").on("click", function(event) {
        /**
         * This function loads the page to administer statuses
         */
        $("#mainrow").load("/administerStatuses/", function() {
            $("#createNewStatusFormLink").click();
        });
    });

    $("#addNewEquipmentLink").on("click", function(event) {
        /**
         * This function loads the add new equipment page
         */
        $("#mainrow").load("/addNewEquipment/", function() {
            $("#createInventoryItemBtn").click();
        });
    });

    $("#collectionAdministrationLink").on("click", function(event) {
        /**
         * This function loads the page to administer collections
         */
        $("#mainrow").load("/administerCollections/", function() {
            $("#createNewCollectionFormLink").click();
        });
    });

    $("#locationAdministrationLink").on("click", function(event) {
        /**
         * This function loads the page to administer collections
         */
        $("#mainrow").load("/administerLocations/", function() {
            $("#createNewLocationFormLink").click();
        });
    });

    $("#buildingAdministrationLink").on("click", function(event) {
        /**
         * This function loads the page to administer collections
         */
        $("#mainrow").load("/administerBuildings/", function() {
            $("#createNewBuildingFormLink").click();
        });
    });

    $("#mainblock").on("click", "#submitRegistrationBtn", function(event) {
        /**
         * This function handles the submission of a new operator registration form.
         */
        var newOperatorForm = $("#registrationForm").serialize();
        $.post("/registerNewUser/", function(response) {
            $("#registrationFormBody").html(response);
        });
    });

    $("#actionTypeAdministrationLink").on("click", function(event) {
        /**
         * This function loads the page to administer Action Types
         */
        $("#mainrow").load("/administerActionTypes/", function() {
            $("#createNewActionTypeFormLink").click();
        });
    });

    $("#viewTodaysActionsLink").on("click", function(event) {
        /**
         * This function loads the today's actions view
         */
        $("#mainrow").load("/viewTodaysActions/", function() {
            loadTodaysActions();
        })
    });

    $("#addNewReservationLink").on("click", function(event) {
        /**
         * This function loads the page to add new reservations
         */
        $("#mainrow").load("/addNewReservation/", function() {
            // This sets up the datepickers in the add action form
            $("#startDateTime").datetimepicker();
            $("#endDateTime").datetimepicker();
            $("#newReservationActions").sortable();
            loadActionTypes();
            loadOrigins();
            loadDestinations();
            loadAssignUserToAction();
            //fillNewReservation();
        });
    });

});