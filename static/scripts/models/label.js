var Label = can.Model.extend({
    findAll: 'GET /labels/',
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/labels/'+params.id,
                type: 'get',
                dataType: 'json'
            });
        } else if (params.LabelName) {
                return $.ajax({
                    url: '/labels/'+params.LabelName,
                    type: 'get',
                    dataType: 'json'
            })
        }
    },
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