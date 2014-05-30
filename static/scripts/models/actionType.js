var ActionType = can.Model({
    findAll: 'GET /actionTypes/',
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/actionTypes/'+params.id,
                type: 'get',
                dataType: 'json'
            });
        } else if (params.ActionTypeName) {
                return $.ajax({
                    url: '/actionTypes/'+params.ActionTypeName,
                    type: 'get',
                    dataType: 'json'
            })
        }
    },
    create:  'POST /actionTypes/',
    update:  'PUT /actionTypes/{id}',
    destroy: 'DELETE /actionTypes/{id}'
}, {})