steal(function() {

    toggleClickText = function(replace) {
        var oldText = replace.text();
        var newText = replace.attr('replace-text');

        if (replace.text(oldText)) {
            replace.text(newText);
        } else {
            replace.text(oldText);
        }

        replace.attr('replace-text',oldText);
    };

    setHide = function(element) {
        element.text('hide');
        element.attr('replace-text','view');
    };

    setView = function(element) {
        element.text('view');
        element.attr('replace-text','hide');
    };

    $("body").on("click", ".header", function (event) {
        $(this).nextUntil('span.header').slideToggle(0);
        toggleClickText($(this).find('span'));
    });

    $("body").on("click", "#showAllItems", function (event) {
        $(".collapse").show();
        $(".header").each(function(index, header) {
            setHide($(this).find('span'));
        });
    });

    $("body").on("click", "#hideAllItems", function (event) {
        $(".collapse").hide();
        $(".header").each(function(index, header) {
            setView($(this).find('span'));
        });
    });

});