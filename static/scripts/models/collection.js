var Collection = can.Model({
    findAll: 'GET /collections/',
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/collections/'+params.id,
                type: 'get',
                dataType: 'json'
            });
        } else if (params.CollectionName) {
                return $.ajax({
                    url: '/collections/'+params.CollectionName,
                    type: 'get',
                    dataType: 'json'
            })
        }
    },
    create:  'POST /collections/',
    update:  'PUT /collections/{id}',
    destroy: 'DELETE /collections/{id}'
}, {})