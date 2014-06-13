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


@api_view([u'GET', u'POST'])
def inventoryItemList(request, format=None):
    '''
    Retrieve a list of all Label Notes
    '''
    if request.method == u'GET':
        inventoryItems = InventoryItem.objects.all()
        serializer = InventoryItemSerializer(inventoryItems, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = InventoryItemSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([u'GET', u'PUT', u'DELETE'])
def inventoryItemDetail(request, pk, format=None):
    '''
    Retrieve, update or delete Inventory Item.
    '''
    try:
        inventoryItem = InventoryItem.objects.get(ItemID=pk)
    except InventoryItem.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == u'GET':
        serializer = InventoryItemSerializer(inventoryItem)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = InventoryItemSerializer(inventoryItem, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        inventoryItem.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view([u'GET', u'POST'])
def consumableItemList():
    pass


@api_view([u'GET', u'PUT', u'DELETE'])
def consumableItemDetail():
    pass


@api_view([u'GET', u'POST'])
def nonInventoryItemList(request, format=None):
    '''
    Retrieve a list of all non Inventory items
    '''
    if request.method == u'GET':
        nonInventoryItems = NonInventoryItem.objects.all()
        serializer = NonInventoryItemSerializer(nonInventoryItems, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = NonInventoryItemSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([u'GET', u'PUT', u'DELETE'])
def nonInventoryItemDetail(request, pk, format=None):
    '''
    Retrieve, update or delete a non Inventory Item.
    '''
    try:
        nonInventoryItem = NonInventoryItem.objects.get(ItemID=pk)
    except NonInventoryItem.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = NonInventoryItemSerializer(nonInventoryItem)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = InventoryItemSerializer(nonInventoryItem, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        nonInventoryItem.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
