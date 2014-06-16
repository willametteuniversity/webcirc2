from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *


@api_view([u'GET', u'POST'])
def labelNoteList(request, format=None):
    '''
    Retrieve a list of all Label Notes
    '''
    if request.method == u'GET':
        labelNotes = LabelNotes.objects.all()
        serializer = LabelNotesSerializer(labelNotes, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = LabelNotesSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([u'GET', u'PUT', u'DELETE'])
def labelNoteDetail(request, pk, format=None):
    '''
    Retrieve, update or delete Label Note.
    '''
    try:
        labelNote = LabelNotes.objects.get(LabelNoteID=pk)
    except LabelNotes.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == u'GET':
        serializer = LabelNotesSerializer(labelNote)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = LabelNotesSerializer(labelNote, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        labelNote.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)