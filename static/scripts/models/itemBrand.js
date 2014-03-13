var ItemBrand = can.Model({
    findAll: 'GET /brands/',
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/brands/'+params.id,
                type: 'get',
                dataType: 'json'
            });
        } else if (params.BrandName) {
                return $.ajax({
                    url: '/brands/'+params.BrandName,
                    type: 'get',
                    dataType: 'json'
            })
        }
    },
    create:  'POST /brands/',
    update:  'PUT /brands/{id}',
    destroy: 'DELETE /brands/{id}'
}, {})