from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *


@csrf_exempt
@api_view([u'GET', u'PUT', u'DELETE'])
def collectionDetail(request, pk=None, cn=None, format=None):
    '''
    Retrieve, update or delete a Collection.
    '''
    try:
        if pk is not None:
            collection = Collection.objects.get(CollectionID=pk)
        elif cn is not None:
            collection = Collection.objects.get(CollectionName=cn)
    except Collection.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = CollectionSerializer(collection, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        collection.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view([u'GET', u'POST'])
def collectionList(request, format=None):
    '''
    Lists all Collections
    '''
    if request.method == u'GET':
        collections = Collection.objects.all()
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = CollectionSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
