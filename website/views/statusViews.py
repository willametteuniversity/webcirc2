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
    This handles a request to display the form for administering statuses.
    '''
    return render(request, u'administer_statuses.html', {})


@csrf_exempt
def addNewStatusForm(request):
    '''
    This handles a request to display the adding a new status form.
    '''
    return render(request, u'forms/add_new_status_form.html', {})


@csrf_exempt
def chooseStatusToEditForm(request):
    '''
    This handles a request to display the edit form for statuses.
    '''
    return render(request, u'forms/choose_status_to_edit_form.html', {})


@api_view([u'GET', u'PUT', u'DELETE'])
def statusDetail(request, pk, format=None):
    '''
    Retrieve, update or delete a Status.
    '''
    # We will use try/except. If Django cannot find an object
    # with the primary key or provided status name we give it using get(), it throws
    # an error.
    try:
        if pk is not None:
            status = Status.objects.get(StatusID=pk)
        elif cn is not None:
            status = Status.objects.get(StatusName=cn)
    except Status.DoesNotExist:
        # If we didn't find it, return a HTTP code of 404
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == u'GET':
        serializer = StatusSerializer(status)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = StatusSerializer(status, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        status.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)