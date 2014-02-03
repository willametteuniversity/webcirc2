var Collection = can.Model({
    findAll: 'GET /collections/',
    findOne: 'GET /collections/{id}',
    create:  'POST /collections/',
    update:  'PUT /collections/{id}',
    destroy: 'DELETE /collections/{id}'
}, {})