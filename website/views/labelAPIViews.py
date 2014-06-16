from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *


@api_view([u'GET', u'POST'])
def labelList(request, format=None):
    '''
    Lists all Labels
    '''
    if request.method == u'GET':
        labels = Label.objects.all()
        serializer = LabelSerializer(labels, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = LabelSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([u'GET', u'PUT', u'DELETE'])
def labelDetail(request, pk=None, ln=None, format=None):
    '''
    Retrieve, update or delete a Label.
    '''
    try:
        if pk is not None:
            label = Label.objects.get(LabelID=pk)
        elif ln is not None:
            label = Label.objects.get(LabelName=ln)
    except Label.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = LabelSerializer(label)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = LabelSerializer(label, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        # If they used DELETE, they want to delete the Collection
        # that they sent the PK for.
        label.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
