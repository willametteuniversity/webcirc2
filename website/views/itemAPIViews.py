from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *

@api_view(['Get'])
def actionItems(request, pk):
    try:
        # get the action object, iterate over the item_set
        # for each item, serialize appropriately
        print InventoryItem.objects.get(ItemID=1)
        item_set = Action.objects.all()
        for item in item_set:
            print item.__class__.__name__
        return Response(ActionSerializer(Action.objects.get(ActionID=pk)).data, status=200)
    except Action.DoesNotExist:
        return Response(status=404)


