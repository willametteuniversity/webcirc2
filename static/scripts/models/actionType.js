var ActionType = can.Model({
    findAll: 'GET /action/',
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/actions/'+params.id,
                type: 'get',
                dataType: 'json'
            });
        } else if (params.ActionTypeName) {
                return $.ajax({
                    url: '/actions/'+params.ActionTypeName,
                    type: 'get',
                    dataType: 'json'
            })
        }
    },
    create:  'POST /actions/',
    update:  'PUT /actions/{id}',
    destroy: 'DELETE /actions/{id}'
}, {})