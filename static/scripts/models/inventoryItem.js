var InventoryItem = can.Model({
    findAll: function(params) {
        steal.dev.log('Find all InventoryItem');
        steal.dev.log(params);
        if (params.eterm) {
            steal.dev.log('Searching inventory item by term..');
            return $.ajax({
                url: '/inventoryItems/'+params.eterm,
                type: 'get',
                dataType: 'json'
            });
        } else if (params.action_id) {
            steal.dev.log('Searching inventory item by action..');
            return $.ajax({
                url: '/actionInventoryItems/'+params.action_id,
                type: 'get',
                dataType: 'json'
            });
        } else {
            steal.dev.log('Getting all inventory items..');
            return $.ajax({
                url: '/inventoryItems/',
                type: 'get',
                dataType: 'json'
            });
        }
    },
    findOne: 'GET /inventoryItems/{id}',
    create:  'POST /inventoryItems/',
    update:  'PUT /inventoryItems/{id}',
    destroy: 'DELETE /inventoryItems/{id}'
}, {});