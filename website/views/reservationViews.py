import json
import re
import pytz

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


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

def checkItemIsAvailableBetweenTimes(item, startTime, endTime):
    '''
    This function checks that a specific piece of equipment is available between a start date and an end date.
    '''
    actions = item.Action.all()
    # First check is to get the action that starts just prior to our desired start time from the actions associated
    # with the item

    # If we can't find a previous action, this is the first action for that piece of equipment, so of course it is
    # available for anything. Absolutely anything.
    try:
        p = actions.filter(StartTime__lte=startTime).order_by(u'-StartTime')[0]
    except IndexError:
        return True

    # Once we have that, we need to make sure it does not end during or after desired time
    if p.EndTime >= endTime:
        return False
    else:
        return True

def previousAction(action):
    try:

        previousAction = Action.objects.filter(EndTime__lt=action.StartTime).order_by(u'-EndTime')[0]
        if previousAction == action:
            return False
    except IndexError:
        return False
    #print "previousAction EndTime: "+str(previousAction.EndTime)
    #print 'Previous action is: '+str(previousAction.ActionID)
    return previousAction

def isDelivery(action, equipment):
    print 'Checking isDelivery for action: '+str(action.ActionID)+' item:'+str(equipment.ItemID)
    if action.Origin != equipment.StorageLocation:
        print "It is not a delivery!"
        return False
    print "It is a delivery!"
    return True

def equipmentComesHomeFirst(action, equipment):
    #print 'Checking equipmentComesHomeFirst for action: '+str(action.ActionID)+' item: '+str(equipment.ItemID)
    pAction = previousAction(action)
    if pAction == False:
        print "No previous action in equipmentComesHomeFirst"
        return True
    if pAction.Destination != equipment.StorageLocation:
        print "Previous action Destination does not equal storagelocation"
        return False
    return True

def addToSchedule(action, equipment):
    if isDelivery(action, equipment):
        if not equipmentComesHomeFirst(action, equipment):
            print "Action: "+str(action.ActionID)+" Equipment: "+str(equipment.ItemID)+ " does not come home first "
            return False
        else:
            print "Action: "+str(action.ActionID)+" Equipment: "+str(equipment.ItemID)+ " does come home first "
            return True
    else:
        pAction = previousAction(action)
        if not pAction:
            print "no Previous action was found"
            return True
        if pAction.Reservation.all()[0] != action.Reservation.all()[0]:
            print "pAction and action Reservation not the same"
            return False
        else:
            print "pAction and action Reservation are the same!"
            print pAction.inventoryitem_set.all()
            if equipment in pAction.inventoryitem_set.all():
                print "Equipment is in the prior delivery action"
                return True
            else:
                print "Equipment is not in the prior delivery action"
                return False

def findAvailableEquipment(request):
    '''
    This function attempts to find an available piece of equipment to fulfill a reservation's needs
    '''
    actions = request.GET.getlist('actions[]')

    equipmentCategory = request.GET['categoryid']
    candidateEquipment = InventoryItem.objects.filter(CategoryID=equipmentCategory)
    print candidateEquipment
    results = {}
    e = None
    for eachAction in actions:
        print "Processing action: "+eachAction
        results[eachAction] = [False]
        curAction = Action.objects.get(ActionID=eachAction)
        for eachEquipment in candidateEquipment:
            if addToSchedule(curAction, eachEquipment):
                eachEquipment.Action.add(curAction)
                # If we do assign something later, we need to keep a reference so that we can use it later if we need
                # to remove it from the actions we've just assigned ito. For example, if the piece of equipment isn't
                # available for 1 out of 6 actions or something
                e = eachEquipment
                results[eachAction] = [True, eachEquipment.ItemID]
                break
            else:
                pass

    responseCode = 200
    print results
    for eachResult in results.values():
        if eachResult[0] == False:
            # If any of the attempts to assign the piece of equipment to an action fail, we need to remove
            # that equipment from all the actions it was assigned too
            if e != None:
                for eachAction in actions:
                    e.Action.remove(eachAction)
            responseCode = 404
            break
    return HttpResponse(json.dumps(results), status=responseCode)

def findAvailableNonInventoryEquipment(request):
    '''
    This function attempts to find an available piece of non-inventory to fulfill a reservation's needs
    '''
    print request.GET
    actions = request.GET.getlist('actions[]')
    equipmentCategory = request.GET['categoryid']
    candidateEquipment = NonInventoryItem.objects.filter(CategoryID=equipmentCategory)
    results = {}
    for eachAction in actions:
        print "Processing action: "+eachAction+" for non-inventory item assignment"
        results[eachAction] = [False]
        curAction = Action.objects.get(ActionID=eachAction)

        for eachEquipment in candidateEquipment:
            if addToSchedule(curAction, eachEquipment):
                eachEquipment.Action.add(curAction)
                results[eachAction] = [True, eachEquipment.ItemID]
                break
            else:
                pass

    responseCode = 200
    print results
    for eachResult in results.values():
        if eachResult[0] == False:
            responseCode = 501
            break
    return HttpResponse(json.dumps(results), status=responseCode)

def findAvailableConsumableEquipment(request):
    '''
    This function attempts to find an available consumable item to fulfill a reservation's needs
    '''
    actions = request.GET.getlist(u'actions[]')
    quantity = int(request.GET[u'quantity'])
    equipmentCategory = request.GET[u'categoryid']
    candidateEquipment = ConsumableItem.objects.filter(CategoryID=equipmentCategory)
    results = {}
    for eachAction in actions:
        print "Processing action: "+eachAction+" for consumable item assignment"
        results[eachAction] = [False]
        curAction = Action.objects.get(ActionID=eachAction)

        for eachEquipment in candidateEquipment:
            if eachEquipment.Quantity >= quantity:
                eachEquipment.Action.add(curAction)
                eachEquipment.Quantity -= quantity
                eachEquipment.save()
                results[eachAction] = [True, eachEquipment.ItemID]
                break
            else:
                results[eachAction] = [False, u'Quantity too low']
                pass

    responseCode = 200
    print results
    for eachResult in results.values():
        if eachResult[0] == False:
            responseCode = 501
            break
    return HttpResponse(json.dumps(results), status=responseCode)