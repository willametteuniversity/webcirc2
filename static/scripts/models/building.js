var Building = can.Model({
    findAll: 'GET /building/',
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/buildings/'+params.id,
                type: 'get',
                dataType: 'json'
            });
        } else if (params.BuildingName) {
                return $.ajax({
                    url: '/buildings/'+params.BuildingName,
                    type: 'get',
                    dataType: 'json'
            })
        }
    },
    create:  'POST /buildings/',
    update:  'PUT /buildings/{id}',
    destroy: 'DELETE /buildings/{id}'
}, {})