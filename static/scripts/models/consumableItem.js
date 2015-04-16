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
                    url: '/consumableItems/'+params.action_id,
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
    findOne: 'GET /consumableitems/{id}',
    create:  'POST /consumableitems/',
    update:  'PUT /consumableitems/{id}',
    destroy: 'DELETE /consumableitems/{id}'
}, {});