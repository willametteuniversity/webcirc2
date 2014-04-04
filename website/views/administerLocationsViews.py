import json
import re

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def administerLocations(request):
    '''
    This handles a request to display the form for administering locations.
    '''
    return render(request, u'administer_locations.html', {})

@csrf_exempt
def addNewLocationForm(request):
    '''
    This handles a request to display the adding a new location form.
    '''
    return render(request, u'forms/add_new_location_form.html', {})

@csrf_exempt
def chooseLocationToEditForm(request):
    '''
    This handles a request to display the edit form for locations.
    '''
    return render(request, u'forms/choose_location_to_edit_form.html', {})