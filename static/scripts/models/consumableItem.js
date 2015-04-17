var ConsumableItem = can.Model({
    findAll: function(params) {
    if (params.eterm) {
                return $.ajax({
                    url: '/consumableItems/'+params.eterm,
                    type: 'get',
                    dataType: 'json'
                });
            } else if (params.action_id) {
                return $.ajax({
                    url: '/actionConsumableItems/'+params.action_id,
                    type: 'get',
                    dataType: 'json'
                });
            } else {
                return $.ajax({
                    url: '/consumableItems/',
                    type: 'get',
                    dataType: 'json'
                });
            }
    },
    findOne: 'GET /consumableItems/{id}',
    create:  'POST /consumableItems/',
    update:  'PUT /consumableItems/{id}',
    destroy: 'DELETE /consumableItems/{id}'
}, {});