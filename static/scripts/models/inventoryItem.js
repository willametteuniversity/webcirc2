var InventoryItem = can.Model({
    findAll: 'GET /inventoryItems/',
    findOne: 'GET /inventoryItems/{id}',
    create:  'POST /inventoryItems/',
    update:  'PUT /inventoryItems/{id}',
    destroy: 'DELETE /inventoryItems/{id}'

}, {});