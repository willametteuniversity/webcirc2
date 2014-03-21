steal(function() {
    $("#mainrow").on("click", "#newReservationFindCustomerBtn", function(event) {
        event.preventDefault();
        // Let's search by their e-mail first
        var userEmail = $("#customerEmail").val();
        User.findOne({id: userEmail}, function(User) {
            steal.dev.log(User);
        }, function(failed) {
            steal.dev.warn("User was not found!");
        });
        steal.dev.log("Find Customer Btn clicked!");
    });

    $("#mainrow").on("click", "#newReservationNewCustomerBtn", function(event) {
        event.preventDefault();
        steal.dev.log("New Customer Btn clicked!");
    });

    $("#mainrow").on("click", "#addNewActionBtn", function(event) {
        event.preventDefault();
        var existingActions = $(".reservationAction");
        if (existingActions.length == 0) {
            var startingPoint = $("#newReservationsActionsHelp").append()
        }
    });

    var constructNewAction = function() {
        
    }
})