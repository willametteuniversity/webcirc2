var Action = can.Model({
    findAll: 'GET /actions/',
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