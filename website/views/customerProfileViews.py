from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *

@api_view(['GET', 'POST'])
def customerProfileList(request):
    '''
    This function handles retrieving a list of Customer Profiles or
    creating a new one.
    '''
    if request.method == u'GET':
        all_profiles = CustomerProfile.objects.all()
        serializer = CustomerProfileSerializer(all_profiles, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = CustomerProfileSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def customerProfileDetail(request, uid=None):
    '''
    This function handles retrieving details about a single user,
    deleting them or updating them.
    '''
    try:
        currentModel = None
        if uid:
            currentModel = CustomerProfile.objects.get(user__pk=uid)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except CustomerProfile.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        if currentModel:
            serializer = CustomerProfileSerializer(currentModel)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = CustomerProfileSerializer(currentModel, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        currentModel.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)