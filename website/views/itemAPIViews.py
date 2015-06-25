from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *
from rest_framework import status
from django.http import HttpResponse


@api_view([u'GET'])
def actionInventoryItems(request, pk):
    try:
        return Response(InventoryItemSerializer(Action.objects.get(ActionID=pk).inventoryitem_set.all(), many=True).data, status=200)
    except Action.DoesNotExist:
        return Response(status=404)


@api_view([u'POST'])
def addInventoryItemToAction(request, pk):
    ## TODO: Make sure the item doesn't conflict
    try:
        item = InventoryItem.objects.get(pk=pk)
        action = Action.objects.get(pk=request.POST['action'])
    except (InventoryItem.DoesNotExist, Action.DoesNotExist):
        return Response(status=404)
    try:
        action.inventoryitem_set.add(item)
    except:
        return Response(status=500)
    return Response(status=201)

# TODO: make sure to call .save() after every db change?

@api_view([u'POST'])
def removeInventoryItemfromAction(request, pk):
    try:
        item = InventoryItem.objects.get(pk=pk)
        action = Action.objects.get(pk=request.POST['action'])
    except (InventoryItem.DoesNotExist, Action.DoesNotExist):
        return Response(status=404)
    try:
        action.inventoryitem_set.remove(item)
    except:
        return Response(status=500)
    return Response(status=200)

@api_view([u'GET', u'POST'])
def inventoryItemList(request, label=None, format=None):
    '''
    Retrieve a list of all Label Notes
    '''
    if request.method == u'GET':
        inventoryItems = InventoryItem.objects.all()
        if label != None:
            itemsWithLabel = ItemLabel.objects.filter(LabelID__LabelName__iexact=label).values(u'ItemID')
            i = []
            for eachItem in itemsWithLabel:
                i.append(InventoryItem.objects.get(pk=eachItem[u'ItemID']))
            inventoryItems = i
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
