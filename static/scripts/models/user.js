var User = can.Model.extend({
    findAll: 'GET /users/',
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/users/'+params.id,
                type: 'get',
                dataType: 'json'
            });
        } else if (params.UserEmail) {
                return $.ajax({
                    url: '/users/'+params.UserEmail,
                    type: 'get',
                    dataType: 'json'
            })
        }
    },
    create:  {
        type: 'POST',
        contentType: 'application/json',
        url: '/users/'
    },
    update:  {
        type: 'PUT',
        contentType: 'application/json',
        url: '/users/{id}'
    },
    destroy: {
        type: 'DELETE',
        contentType: 'application/json',
        url: '/users/{id}'
    }

}, {})