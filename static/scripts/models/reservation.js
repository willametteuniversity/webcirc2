var Reservation = can.Model({
    id: "ReservationID",
    findAll: 'GET /reservations/',
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/reservations/'+params.id,
                type: 'get',
                dataType: 'json'
            });
        }
    },
    create:  'POST /reservations/',
    update:  'PUT /reservations/{id}',
    destroy: 'DELETE /reservations/{id}'
}, {})