var InventoryItem = can.Model({
    findAll: 'GET /inventoryitems/',
    findOne: 'GET /inventoryitems/{id}',
    create:  'POST /inventoryitems/',
    update:  'PUT /inventoryitems/{id}',
    destroy: 'DELETE /inventoryitems/{id}'
}, {});