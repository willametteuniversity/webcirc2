steal(function() {

    $('#saveNewLabelBtn').on('click', function(event) {
        event.preventDefault();
        var newLabel = new Label({LabelName: $('#newLabelNameText').val()});
        newLabel.save(function(saved) {
            $('#closeAddNewLabelModalBtn').click();
            loadLabels();
        });
    });

    $('#mainrow').on('click', '#delLabelBtn', function(event) {
        event.preventDefault();
        var labelToDelete = $('#labelListBox').val();
        for (x = 0; x < labelToDelete.length; x++) {
            Label.destroy(labelToDelete[x]).then(function() {
                loadLabels();
            });
        }
    });

    $('#mainrow').on('click', '#addCategoryBtn', function(event) {
        event.preventDefault();
        $('#addNewCategoryModal').modal('show');
    });

    $('#saveNewCategoryBtn').on('click', function(event) {
        event.preventDefault();
        var parentID = $('#categoryMasterTree').jstree().get_selected()[0];
        steal.dev.log('Creating new category. Parent:');
        steal.dev.log(parentID);
        var newCategory = new Label({LabelName: $('#newCategoryNameText').val(),
                                    ParentCategory: parentID});
        newCategory.save(function(saved){
            steal.dev.log('New category saved');
            $('#categoryMasterTree').jstree('refresh');
        })
    });

    $('#mainrow').on('click', '#delCategoryBtn', function(event) {
        event.preventDefault();
        var categoryToDelete = $('#categoryMasterTree').jstree().get_selected()[0];
        steal.dev.log('Deleting category...');
        // TODO: Should use a prototype method so we get a callback and can confirm it was deleted?
        Label.destroy(categoryToDelete).then(function() {
            $('#categoryMasterTree').jstree('refresh');
        });

    });

});