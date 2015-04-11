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
import datetime


@csrf_exempt
def addNewReservation(request):
    '''
    This handles a request to display the page for adding a new reservation.
    '''
    return render(request, u'add_new_reservation.html', {})

@csrf_exempt
def addNewReservationForm(request):
    '''
    This handles a request to display the form for adding a new reservation
    '''
    return render(request, u'forms/add_new_reservation_form.html', {})

def previousAction(action):
    print 'Checking previousAction for: '+str(action.ActionID)
    previousAction = Action.objects.filter(EndTime__lt=action.StartTime).order_by(u'-EndTime')[0]
    print 'Previous action is: '+str(previousAction.ActionID)
    return previousAction

def isDelivery(action, equipment):
    print 'Checking isDelivery for: '+str(action.ActionID)+' '+str(equipment.ItemID)
    if action.Origin != equipment.StorageLocation:
        return False
    return True

def equipmentComesHomeFirst(action, equipment):
    print 'Checking equipmentComesHomeFirst for: '+str(action.ActionID)+' '+str(equipment.ItemID)
    if previousAction(action).Destination != equipment.StorageLocation:
        return False
    return True

def addToSchedule(action, equipment):
    if isDelivery(action, equipment):
        if not equipmentComesHomeFirst(action, equipment):
            print "Equipment does not come home first!"
            return False
        else:
            print "Equipment comes home first!"
            return True
    else:
        print previousAction(action).Reservation.all()[0]
        print action.Reservation.all()[0]
        if previousAction(action).Reservation.all()[0] != action.Reservation.all()[0]:
            print "Previous action and action reservations are not the same!"
            return False
        else:
            print "Previous action and action reservations are the same!"
            return True

def findAvailableEquipment(request):
    '''
    This function attempts to find an available piece of equipment to fulfill a reservation's needs
    '''

    actions = request.GET['actions[]'].split(",")
    equipmentCategory = request.GET['categoryid']
    candidateEquipment = InventoryItem.objects.filter(CategoryID=equipmentCategory)
    print 'Candidate equipment is: '
    for q in candidateEquipment:
        print q.ItemID
    print '----'
    for eachAction in actions:
        print "Retrieving action "+eachAction
        curAction = Action.objects.get(ActionID=eachAction)
        for eachEquipment in candidateEquipment:
            if addToSchedule(curAction, eachEquipment):
                print "Found an acceptable piece of equipment!"
            else:
                print "This piece of equipment does not work, trying another one!"

    return HttpResponse(200)