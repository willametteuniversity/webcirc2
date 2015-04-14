steal(function() {


    $("body").on("click", ".header", function (event) {
        $(this).nextUntil('span.header').slideToggle(0);
    });

    $("body").on("click", "#showAllItems", function (event) {
        $(".collapse").slideToggle(0)
    });

});