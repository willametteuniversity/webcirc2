var ItemModel = can.Model({
    findAll: 'GET /models/',
    findOne: 'GET /models/{id}',
    create:  'POST /models/',
    update:  'PUT /models/{id}',
    destroy: 'DELETE /models/{id}'
}, {})