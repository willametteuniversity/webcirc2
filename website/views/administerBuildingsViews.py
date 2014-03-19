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

# Django REST Framework imports
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Our application imports
from website.models import *
from website.serializers import *

@csrf_exempt
def administerBuildings(request):
    '''
    This handles a request to display the form for administering buildings.
    '''
    return render(request, u'administer_buildings.html', {})

@csrf_exempt
def addNewBuildingForm(request):
    '''
    This handles a request to display the adding a new building form.
    '''
    return render(request, u'forms/add_new_building_form.html', {})

@csrf_exempt
def chooseBuildingToEditForm(request):
    '''
    This handles a request to display the edit form for buildings.
    '''
    return render(request, u'forms/choose_building_to_edit_form.html', {})