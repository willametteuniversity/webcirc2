from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *


@api_view([u'GET', u'POST'])
def imageList(request, format=None):
    '''
    Retrieve a list of all Label Notes
    '''
    if request.method == u'GET':
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = ImageSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([u'GET', u'PUT', u'DELETE'])
def imageDetail(request, pk, format=None):
    '''
    Retrieve, update or delete Label Note.
    '''
    try:
        image = Image.objects.get(ImageID=pk)
    except Image.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = ImageSerializer(image)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = ImageSerializer(image, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        image.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)