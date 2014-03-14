var NonInventoryItem = can.Model({
    findAll: 'GET /noninventoryitems/',
    findOne: 'GET /noninventoryitems/{id}',
    create:  'POST /noninventoryitems/',
    update:  'PUT /noninventoryitems/{id}',
    destroy: 'DELETE /noninventoryitems/{id}'
}, {});