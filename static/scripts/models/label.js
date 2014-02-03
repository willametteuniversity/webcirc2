var Label = can.Model({
    findAll: 'GET /labels/',
    findOne: 'GET /labels/{id}',
    create:  'POST /labels/',
    update:  'PUT /labels/{id}',
    destroy: 'DELETE /labels/{id}'
}, {})