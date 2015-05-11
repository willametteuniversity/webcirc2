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


def index(request):
    '''
    This function handles returning the index page. First page the user visits.
    '''
    template = loader.get_template(u'webcirc2.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def registerNewUser(request):
    '''
    This function handles requests relating to registering a new user
    '''

    if request.GET:
        # Is there any reason we would be doing GET to this URL?
        # TODO: Refactor this to use the 501 redirection and create a 501 page
        return HttpResponse(status=501)
    elif request.POST:
        # This means we need to register a new user
        # First let's make sure we got all of the needed information.
        responseData = {}
        if u'username' not in request.POST:
            responseData[u'result'] = u'failed'
            responseData[u'reason'] = u'A username is required.'
            return HttpResponse(json.dumps(responseData), content_type=u'application/json')
        if u'email' not in request.POST:
            responseData[u'result'] = u'failed'
            responseData[u'reason'] = u'An e-mail is required.'
            return HttpResponse(json.dumps(responseData), content_type=u'application/json')
        if u'password' not in request.POST:
            responseData[u'result'] = u'failed'
            responseData[u'reason'] = u'A password is required.'
            return HttpResponse(json.dumps(responseData), content_type=u'application/json')
        if u'confirmPassword' not in request.POST:
            responseData[u'result'] = u'failed'
            responseData[u'reason'] = u'Password confirmation is required.'
            return HttpResponse(json.dumps(responseData), content_type=u'application/json')

        # Now we need to check if the username is too long
        if len(request.POST[u'username']) > 15:
            responseData[u'result'] = u'failed'
            responseData[u'reason'] = u'Username too long.'
            return HttpResponse(json.dumps(responseData), content_type=u'application/json')

        # Check to make sure there are only alphanumeric characters in the username
        if not re.match(r'^[A-z0-9]*$', request.POST[u'username']):
            responseData[u'result'] = u'failed'
            responseData[u'reason'] = u'Username field contained improper characters.'
            return HttpResponse(json.dumps(responseData), content_type=u'application/json')

        # Now let's make sure the password and confirm password match
        if request.POST[u'password'] != request.POST[u'confirmPassword']:
            responseData[u'result'] = u'failed'
            responseData[u'reason'] = u'Passwords did not match.'
            return HttpResponse(json.dumps(responseData), content_type=u'application/json')

        # Let's make sure a user with that username doesn't already exist, using a
        # case-insensitive search
        u = User.objects.filter(username__iexact=request.POST[u'username']).count()
        if u > 0:
            # We know one already exists with that username, so send back an error
            responseData = {}
            responseData[u'result'] = u'failed'
            responseData[u'reason'] = u'A user with that name already exists!'
            return HttpResponse(json.dumps(responseData), content_type=u'application/json')

        # Now let's check for users with the same e-mail address
        u = User.objects.filter(email__iexact=request.POST[u'email']).count()
        if u > 0:
            # We know one already exists with that username, so send back an error
            responseData = {}
            responseData[u'result'] = u'failed'
            responseData[u'reason'] = u'A user with that e-mail already exists!'
            return HttpResponse(json.dumps(responseData), content_type=u'application/json')

        # If we are here, we know the user does not exist, so let's make them
        newUser = User.objects.create_user(request.POST[u'username'], request.POST[u'email'],
                                           request.POST[u'password'])
        newUser.save()
        responseData = {}
        responseData[u'result'] = u'succeeded'
        return HttpResponse(json.dumps(responseData), content_type=u'application/json')

    else:
        # This means we need to display the register new user form
        # Let's load the form up
        return render(request, u'forms/register.html', {})


@csrf_exempt
def login(request):
    '''
    This function handles the logging in of a user, and the submission of the login form from
    the main page.
    '''
    # Set up the response data dict
    responseData = {}

    # First let's check if there is a username and password present in the request
    # Make sure username was included
    if u'username' not in request.POST:
        responseData[u'result'] = u'failed'
        responseData[u'reason'] = u'Username not specified.'
        return HttpResponse(json.dumps(responseData), content_type=u'application/json')

    # Make sure a password was included
    if u'password' not in request.POST:
        responseData[u'result'] = u'failed'
        responseData[u'reason'] = u'Password not specified.'
        return HttpResponse(json.dumps(responseData), content_type=u'application/json')

    # Now let's try to log them in
    u = authenticate(username=request.POST[u'username'], password=request.POST[u'password'])

    # If it is none, login returned a user which means they logged in successfully
    if u is not None:
        # TODO: Check here for is_active?
        django_login(request, u)
        responseData[u'result'] = u'succeeded'
        return HttpResponse(json.dumps(responseData), content_type=u'application/json')
    # If we get here, authentication failed.
    else:
        responseData[u'result'] = u'failed'
        responseData[u'reason'] = u'Invalid username or password.'
        return HttpResponse(json.dumps(responseData), content_type=u'application/json')


def labelAndCategoryMgmt(request):
    '''
    This function returns the label and category management HTML
    '''
    return render(request, u'label_category_mgmt.html', {})

def addNewEquipment(request):
    '''
    This function returns the initial page for adding new equipment
    '''
    return render(request, u'add_new_equipment.html', {})

def addNewInventoryItemForm(request):
    '''
    This function returns the form for adding a new inventory item
    '''
    return render(request, u'forms/add_new_inventory_item_form.html')

def addNewNonInventoryItemForm(request):
    '''
    This function returns the form for adding a new inventory item
    '''
    return render(request, u'forms/add_new_non_inventory_item_form.html')

def addNewConsumableItemForm(request):
    '''
    This function returns the form for adding a new consumable item
    '''
    return render(request, u'forms/add_new_consumable_item_form.html')


@api_view([u'GET'])
def labelsNotCategories(request):
    labels_without_parents = list(Label.objects.filter(ParentCategory=None))
    all_labels = list(Label.objects.all())
    labels_not_categories = labels_without_parents
    for label in all_labels:
        for potential_parent in labels_without_parents:
            if label.ParentCategory == potential_parent:
                labels_not_categories.remove(potential_parent)
    label_serializer = LabelSerializer(labels_not_categories, many=True)
    return Response(label_serializer.data, status=201)


@api_view([u'GET'])
def itemHistoryDetail(request, fk):
    history = ItemHistory.objects.filter(ItemID=fk).order_by(u"ChangeDateTime").reverse()
    if len(history) is 0:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    return Response(ItemHistorySerializer(history, many=True).data, status=201)


@api_view(['GET'])
def reservationHistoryDetail(request, fk):
    history = ReservationHistory.objects.filter(ReservationID=fk).order_by(u"ChangeDateTime").reverse()
    if len(history) is 0:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    return Response(ItemHistorySerializer(history, many=True).data, status=201)


@api_view([u'GET'])
def categoryHierarchy(request):
    #retrive a list of categories in a hierarchy structure
    if request.method == u'GET':
        root = Label.objects.get(pk=1)

        def get_nodes(node):
            d = {}
            children = get_children(node=node)
            d[u'id'] = node.pk
            d[u'text'] = node.LabelName
            d[u'children'] = [get_nodes(x) for x in children]
            return d

        def get_children(node):
            return Label.objects.filter(ParentCategory=node.pk)

        tree = get_nodes(node=root)
        return HttpResponse(json.dumps(tree), content_type=u'application/json')

@api_view([u'GET'])
def categoryHierarchyWithEquipment(request, root=None):
    if request.method == u'GET':
        if root:
            root = Label.objects.get(LabelName=root)
        else:
            root = Label.objects.get(pk=1)

        def get_nodes(node):
            d = {}
            ci, cl, li = get_children(node=node)
            print ci, cl, node

            d[u'id'] = node.pk
            d[u'text'] = node.LabelName
            d[u'children'] = []
            for eachCi in ci:
                d[u'children'].append('#'+str(eachCi.ItemID)+' '+eachCi.BrandID.BrandName+' '+eachCi.ModelID.ModelDesignation)
            for eachChildLabel in cl:
                d[u'children'].append(get_nodes(eachChildLabel))
            for eachChildLabeledItem in li:
                d[u'children'].append('#'+str(eachChildLabeledItem.ItemID.ItemID)+' '+eachChildLabeledItem.ItemID.BrandID.BrandName+' '+
                                        eachChildLabeledItem.ItemID.ModelID.ModelDesignation)
            return d

        def get_children(node):
            c = []
            inventoryItems = InventoryItem.objects.filter(CategoryID=node.pk)
            labeledItems = ItemLabel.objects.filter(LabelID=node.pk)
            for eachItem in inventoryItems:
                c.append(eachItem)
            labelItems = Label.objects.filter(ParentCategory=node.pk)
            for eachItem in labelItems:
                c.append(eachItem)
            print c
            return inventoryItems, labelItems, labeledItems

        tree = get_nodes(node=root)
        return HttpResponse(json.dumps(tree), content_type=u'application/json')

def autocomplete(request):
    '''
    This function takes a search token and a model, and returns autocomplete results to the client.
    '''
    results = []
    if request.GET[u'model'].lower() == u'brand':
        r = ItemBrand.objects.filter(BrandName__icontains = request.GET[u'term'])
        for eachResult in r:
            results.append({u'BrandID': eachResult.BrandID, u'BrandName':eachResult.BrandName})

    elif request.GET[u'model'].lower() == u'model':
        r = ItemModel.objects.filter(ModelDesignation__icontains = request.GET[u'term'])
        for eachResult in r:
            results.append({u'ModelID': eachResult.ModelID, u'ModelDesignation':eachResult.ModelDesignation})

    elif request.GET[u'model'].lower() == u'collection':
        r = Collection.objects.filter(CollectionName__icontains = request.GET[u'term'])
        for eachResult in r:
            results.append({u'CollectionID': eachResult.CollectionID, u'CollectionName': eachResult.CollectionName})

    elif request.GET[u'model'].lower() == u'category':
        r = Label.objects.filter(LabelName__icontains = request.GET[u'term']).exclude(ParentCategory = None)
        for eachResult in r:
            results.append({u'LabelID': eachResult.LabelID, u'LabelName': eachResult.LabelName})

    elif request.GET[u'model'].lower() == u'collection':
        r = Label.objects.filter(CollectionName__icontains = request.GET[u'term'])
        for eachResult in r:
            results.append({u'CollectionID': eachResult.CollectionID, u'CollectionName': eachResult.CollectionName})

    elif request.GET[u'model'].lower() == u'items':
        r = Label.objects.filter(Q(LabelName__icontains = request.GET[u'term']))
        for eachResult in r:
            results.append({u'LabelID': eachResult.LabelID, u'LabelName': eachResult.LabelName})

    return HttpResponse(json.dumps(results), content_type=u'application/json')


# def checkAvailable(item, startTime, endTime):
#     actionItems = ActionItem.objects.filter(InventoryItemID=item.pk)
#     startDate = datetime.strptime(startTime, "%d-%m-%Y %H:%M:%S")
#     endDate = datetime.strptime(endTime, "%d-%m-%Y %H:%M:%S")
#     if not actionItem:
#         return true
#     else:
#         actions = Action.objects.filter(ActionID=[x.ActionID for x in actionItems])
#         for action in actions:
#             actionStartDate = datetime.strptime(action.startTime, "%d-%m-%Y %H:%M:%S")
#             actionEndDate = datetime.strptime(action.endTime, "%d-%m-%Y %H:%M:%S")
#
#             if actionStartDate <= startDate and startDate <= actionEndDate:
#                 return false
#             elif actionStartDate <= endDate and endDate <= actionEndDate:
#                 return false
#             elif actionStartDate >= startDate and actionEndDate <= endDate:
#                 return false
#             elif actionStartDate <= startDate and actionEndDate >= endDate:
#                 return false
#         return true
