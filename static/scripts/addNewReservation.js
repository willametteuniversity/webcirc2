steal(function() {
    $("#mainrow").on("click", "#newReservationFindCustomerBtn", function(event) {
        event.preventDefault();
        steal.dev.log("Find Customer Btn clicked!");
    });
    $("#mainrow").on("click", "#newReservationNewCustomerBtn", function(event) {
        event.preventDefault();
        steal.dev.log("New Customer Btn clicked!");
    });
})