from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *

@api_view(['Get'])
def actionItems(request, pk):
    try:
        # get the action object, iterate over the item_set
        # for each item, serialize appropriately
        item_set = Action.objects.get(ActionID=pk).inventoryitem_set.all()
        for item in item_set:
            print item.__class__.__name__
        return Response(InventoryItemSerializer(Action.objects.get(ActionID=pk).inventoryitem_set.all(), many=True).data, status=200)
    except Reservation.DoesNotExist:
        return Response(status=404)


