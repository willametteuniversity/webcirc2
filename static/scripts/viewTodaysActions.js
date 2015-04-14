steal(function() {


    $("body").on("click", ".header", function (event) {
        $(this).nextUntil('span.header').slideToggle(0);
    });

    $("body").on("click", "#showAllItems", function (event) {
        $(".collapse").show()
    });

    $("body").on("click", "#hideAllItems", function (event) {
        $(".collapse").hide()
    });

});