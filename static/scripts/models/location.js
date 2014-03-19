var Collection = can.Model({
    findAll: 'GET /locations/',
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/locations/'+params.id,
                type: 'get',
                dataType: 'json'
            });
        } else if (params.CollectionName) {
                return $.ajax({
                    url: '/locations/'+params.CollectionName,
                    type: 'get',
                    dataType: 'json'
            })
        }
    },
    create:  'POST /locations/',
    update:  'PUT /locations/{id}',
    destroy: 'DELETE /locations/{id}'
}, {})
