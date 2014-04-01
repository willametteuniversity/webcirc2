var ConsumableItem = can.Model({
    findAll: 'GET /consumableitems/',
    findOne: 'GET /consumableitems/{id}',
    create:  'POST /consumableitems/',
    update:  'PUT /consumableitems/{id}',
    destroy: 'DELETE /consumableitems/{id}'
}, {});