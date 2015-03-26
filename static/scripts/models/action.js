var Action = can.Model({
    findAll: function(params) {
        if (params.date) {
            return $.ajax({
                url: '/actions/'+params.date,
                type: 'get',
                dataType: 'json'
            });
        } else {
            return $.ajax({
                url: '/actions/',
                type: 'get',
                dataType: 'json'
            });
        }
    },
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/actions/'+params.id,
                type: 'get',
                dataType: 'json'
            });
        }
    },
    create:  'POST /actions/',
    update:  'PUT /actions/{id}',
    destroy: 'DELETE /actions/{id}'
}, {})