from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *


@api_view([u'GET', u'POST'])
def itemModelList(request):
    if request.method == u'GET':
        all_models = ItemModel.objects.all()
        serializer = ItemModelSerializer(all_models)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = ItemModelSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([u'GET', u'PUT', u'DELETE'])
def itemModelDetail(request, pk=None, mn=None):
    try:
        if pk is not None:
            current_model = ItemModel.objects.get(ModelID=pk)
        elif mn is not None:
            current_model = ItemModel.objects.get(ModelDesignation=mn)
    except ItemModel.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = ItemModelSerializer(current_model)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = ItemModelSerializer(current_model, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        current_model.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)