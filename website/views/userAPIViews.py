from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *
from django.http import HttpResponse
from rest_framework import status
from django.db.models import Q


@api_view(['GET', 'POST'])
def userList(request):
    '''
    This function handles retrieving a list of Users or
    creating a new one.
    '''
    # TODO: Is this even necessary? What about security concerns?
    if request.method == u'GET':
        all_users = User.objects.all()
        serializer = UserSerializer(all_users, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = UserSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def userDetail(request, pk=None, em=None, fn=None, n=None):
    '''
    This function handles retrieving details about a single user,
    deleting them or updating them
    '''
    try:
        current_model = None
        userModels = None
        if pk:
            current_model = User.objects.get(id=pk)
        elif em:
            current_model = User.objects.get(email=em)
        elif fn:
            firstName, lastName = fn.split(" ", 1)
            userModels = User.objects.filter(first_name=firstName, last_name=lastName)
            if len(userModels) == 0:
                raise User.DoesNotExist
        elif n:
            userModels = User.objects.filter(Q(first_name=n) | Q(last_name=n))
            if len(userModels) == 0:
                raise User.DoesNotExist
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        if current_model:
            serializer = UserSerializer(current_model)
        elif userModels:
            serializer = UserSerializer(userModels, many=True)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = UserSerializer(current_model, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        current_model.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
