var Status = can.Model({
    findAll: 'GET /statuses/',
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/statuses/'+params.id,
                type: 'get',
                dataType: 'json'
            });
        } else if (params.StatusDescription) {
                return $.ajax({
                    url: '/statuses/'+params.StatusDescription,
                    type: 'get',
                    dataType: 'json'
            })
        }
    },
    create:  'POST /statuses/',
    update:  'PUT /statuses/{id}',
    destroy: 'DELETE /statuses/{id}'
}, {})