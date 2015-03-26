from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *


@api_view([u'GET', u'POST'])
def actionTypeList(request):
    if request.method == u'GET':
        all_models = ActionType.objects.all()
        serializer = ActionTypeSerializer(all_models, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = ActionTypeSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([u'GET', u'PUT', u'DELETE'])
def actionTypeDetail(request, pk):
    try:
        current_model = ActionType.objects.get(ActionTypeID=pk)
    except ActionType.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = ActionTypeSerializer(current_model)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = ActionTypeSerializer(current_model, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        current_model.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
