from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *


@csrf_exempt
@api_view([u'GET', u'PUT', u'DELETE'])
def buildingDetail(request, pk=None, bc=None):
    '''
    Retrieve, update or delete a Building.
    '''
    try:
        if pk is not None:
            building = Building.objects.get(BuildingID=pk)
        elif bc is not None:
            building = Building.objects.get(BuildingCode=bc)
    except Building.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = BuildingSerializer(building)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = BuildingSerializer(building, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        building.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@api_view([u'GET', u'POST'])
def buildingList(request):
    '''
    Lists all Buildings
    '''
    if request.method == u'GET':
        buildings = Building.objects.all()
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = BuildingSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)