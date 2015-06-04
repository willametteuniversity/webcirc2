var NonInventoryItem = can.Model({
    findAll: function(params) {
        if (params.eterm) {
            return $.ajax({
                url: '/nonInventoryItems/'+params.eterm,
                type: 'get',
                dataType: 'json'
            });
        } else if (params.action_id) {
            return $.ajax({
                url: '/actionNonInventoryItems/'+params.action_id,
                type: 'get',
                dataType: 'json'
            });
        } else {
            return $.ajax({
                url: '/nonInventoryItems/',
                type: 'get',
                dataType: 'json'
            });
        }
    },
    findOne: 'GET /nonInventoryItems/{id}',
    create:  'POST /nonInventoryItems/',
    update:  'PUT /nonInventoryItems/{id}',
    destroy: 'DELETE /nonInventoryItems/{id}'
}, {});