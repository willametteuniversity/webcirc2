from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *


@api_view(['Get'])
def actionInventoryItems(request, pk):
    try:
        return Response(InventoryItemSerializer(Action.objects.get(ActionID=pk).inventoryitem_set.all(), many=True).data, status=200)
    except Action.DoesNotExist:
        return Response(status=404)


@api_view(['Get'])
def actionConsumableItems(request, pk):
    try:
        return Response(ConsumableItemSerializer(Action.objects.get(ActionID=pk).consumableitem_set.all(), many=True).data, status=200)
    except Action.DoesNotExist:
        return Response(status=404)


@api_view(['Get'])
def actionNonInventoryItems(request, pk):
    try:
        return Response(NonInventoryItemSerializer(Action.objects.get(ActionID=pk).noninventoryitem_set.all(), many=True).data, status=200)
    except Action.DoesNotExist:
        return Response(status=404)


# Create normal Item APIs