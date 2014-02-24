var Label = can.Model.extend({
    findAll: 'GET /labels/',
    findOne: 'GET /labels/{id}',
    create:  {
        type: 'POST',
        contentType: 'application/json',
        url: '/labels/'
    },
    update:  {
        type: 'PUT',
        contentType: 'application/json',
        url: '/labels/{id}'
    },
    destroy: {
        type: 'DELETE',
        contentType: 'application/json',
        url: '/labels/{id}'
    }

}, {})