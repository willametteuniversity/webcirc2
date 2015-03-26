var ItemModel = can.Model({
    findAll: 'GET /models/',
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/models/'+params.id,
                type: 'get',
                dataType: 'json'
            });
        } else if (params.ModelName) {
                return $.ajax({
                    url: '/models/'+params.ModelName,
                    type: 'get',
                    dataType: 'json'
            })
        }
    },
    create:  'POST /models/',
    update:  'PUT /models/{id}',
    destroy: 'DELETE /models/{id}'
}, {})