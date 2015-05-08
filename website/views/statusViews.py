import json
import re

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Auth imports
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.db.models import Q

# Django REST Framework imports
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Our application imports
from website.models import *
from website.serializers import *
from django.core import serializers

from datetime import datetime


@csrf_exempt
def administerStatuses(request):
    '''
    This handles a request to display the form for administering action states.
    '''
    return render(request, u'administer_statuses.html', {})


@csrf_exempt
def addNewStatusForm(request):
    '''
    This handles a request to display the adding a new action state form.
    '''
    return render(request, u'forms/add_new_status_form.html', {})


@csrf_exempt
def chooseStatusToEditForm(request):
    '''
    This handles a request to display the edit form for action states.
    '''
    return render(request, u'forms/choose_status_to_edit_form.html', {})


@api_view([u'GET', u'PUT', u'DELETE'])
def statusDetail(request, pk):
    '''
    Retrieve, update or delete a Status.
    '''
    try:
        current_status = Status.objects.get(StatusID=pk)
    except Status.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = StatusSerializer(current_status)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = StatusSerializer(current_status, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        current_status.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view([u'GET', u'POST'])
def statusList(request, format=None):
    '''
    Retrieve a list of all Label Notes
    '''
    if request.method == u'GET':
        states = Status.objects.all()
        serializer = StatusSerializer(states, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = StatusSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
