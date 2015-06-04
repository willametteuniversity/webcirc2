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

    $("body").on("click", "#loadActionsForDateBtn", function (event) {
        event.preventDefault();
        var dateToLoad = $("#viewActionsByDate").data('date');
        var fDateToLoad = new Date(dateToLoad);
        loadTodaysActions(fDateToLoad);
    });

    $("body").on("click", "#actionDetailModalButton", function (event) {
        var span = event.currentTarget.getElementsByTagName('span')[0];
        console.log("Populating modal with action", span.id, "and reservation", span.getAttribute('reservation'));
        $("#actionDetailModal").modal('show');
    });

    $("#actionDetailModalClose").click(function (event) {
        $("#actionDetailModal").modal('hide');
    });

    $("body").on("click", ".actionstate", function (event) {
        var action_id = event.currentTarget.getAttribute('action');
        var new_action_state = event.currentTarget.getAttribute('state');
        Action.findOne({id: action_id}, function(action) {
            action.attr('id', action.ActionID);
            action.attr('Reservation', action.Reservation[0])
            action.attr("ActionState", new_action_state);
            action.save(function(saved) {
                loadTodaysActions(new Date($("#viewActionsByDate").data('date')));
            });
        });
    });

});