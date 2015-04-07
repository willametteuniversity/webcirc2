var Action = can.Model({
    findAll: function(params) {
        if (params.date) {
            return $.ajax({
                url: '/actions/'+params.date,
                type: 'get',
                dataType: 'json'
            });
        } else {
            return $.ajax({
                url: '/actions/',
                type: 'get',
                dataType: 'json'
            });
        }
    },
    findOne: function(params) {
        if (params.id) {
            return $.ajax({
                url: '/actions/'+params.id,
                type: 'get',
                dataType: 'json'
            });
        }
    },
//    getEquipment: function(params) {
//        var deferred = new can.Deferred();
//        if (params.id) {
//            $.ajax({
//                url: '/actionInventoryItems/'+params.id,
//                type: 'get'
//            }).then(function(data) {
//                deferred.resolve(InventoryItem.models(data || []));
//            }, function(xhr, textStatus, err) {
//                deferred.reject(err);
//            });
//        }
//        //console.log(deferred);
//        //return deferred;
//        deferred.done(function(results){
//            console.log(results);
//            return results;
//        });
//    },
    create:  'POST /actions/',
    update:  'PUT /actions/{id}',
    destroy: 'DELETE /actions/{id}'
}, {})