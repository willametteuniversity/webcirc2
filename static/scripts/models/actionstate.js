var ActionState = can.Model({
    findAll: 'GET /actionstates/',
    //findAll: function() {
    //    return $.ajax({
    //        url: '/actionstates/'
    //        type: 'get',
    //        dataType: 'json'
    //    });
    //},
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/actionstates/'+params.id,
                type: 'get',
                dataType: 'json'
            });
        }
    },
    create:  'POST /actionstates/',
    update:  'PUT /actionstates/{id}',
    destroy: 'DELETE /actionstates/{id}'
}, {})