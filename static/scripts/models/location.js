var Location = can.Model({
    findAll: 'GET /locations/',
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/locations/'+params.id,
                type: 'GET',
                contentType: 'application/json'
            });
        } else if (params.LocationName) {
                return $.ajax({
                    url: '/locations/'+params.CollectionName,
                    type: 'GET',
                    contentType: 'application/json'
            })
        }
    },
    create:  {
        type: 'POST',
        contentType: 'application/json',
        url: '/locations/'
    },
    update:  {
        type: 'PUT',
        contentType: 'application/json',
        url: '/locations/{id}'
    },
    destroy: {
        type: 'DELETE',
        contentType: 'application/json',
        url: '/locations/{id}'
    }
}, {})
