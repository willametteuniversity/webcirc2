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

@csrf_exempt
@api_view([u'GET', u'PUT', u'DELETE'])
def collectionDetail(request, pk=None, cn=None, format=None):
    '''
    Retrieve, update or delete a Collection.
    '''
    # We will use try/except. If Django cannot find an object
    # with the primary key or provided collection name we give it using get(), it throws
    # an error.
    try:
        if pk is not None:
            collection = Collection.objects.get(CollectionID=pk)
        elif cn is not None:
            collection = Collection.objects.get(CollectionName=cn)
    except Collection.DoesNotExist:
        # If we didn't find it, return a HTTP code of 404
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # Again we check for the method and do a different
    # thing depending on which method the client used.
    if request.method == u'GET':
        # If they used GET, we want to retrieve, serialize
        # and send back the particular Collection they
        # requested.
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == u'PUT':
        # If they used PUT, they want to change an already
        # existing collection. So, we deserialize the JSON
        # data the client sent, check if it is valid, and if
        # it is, save it to the DB and send back a success
        # HTTP code.
        serializer = CollectionSerializer(collection, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # If the JSON they sent was not valid, send back
        # the errors from the serializer, and a HTTP status
        # code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        # If they used DELETE, they want to delete the Collection
        # that they sent the PK for.
        collection.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view([u'GET', u'PUT', u'DELETE'])
def buildingDetail(request, pk=None, bc=None, format=None):
    '''
    Retrieve, update or delete a Building.
    '''
    try:
        if pk is not None:
            building = Building.objects.get(BuildingID=pk)
        elif bc is not None:
            building = Building.objects.get(BuildingCode=bc)
    except Building.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = BuildingSerializer(building)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = BuildingSerializer(building, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        building.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@api_view([u'GET', u'POST'])
def buildingList(request, format=None):
    '''
    Lists all Buildings
    '''
    if request.method == u'GET':
        buildings = Building.objects.all()
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = BuildingSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([u'GET', u'POST'])
def collectionList(request, format=None):
    '''
    Lists all Collections
    '''
    # This checks if the method of a request is GET. Remember that
    # when you want to retrieve data from the server, you use
    # GET. When you just visit a website, that's a GET, for
    # example. You can always check the "method" attribute of
    # a request object in Django to get the type of request.
    if request.method == u'GET':
        # Here we retrieve all of our Collection instances.
        collections = Collection.objects.all()
        # Here we instantiate our CollectionSerializer. Note that
        # we feed it many=True, so that it knows we are giving it
        # more than one. all() returns a QuerySet object, not just
        # a single instance.
        serializer = CollectionSerializer(collections, many=True)
        # And here we return the serializer's data as JSON. See
        # the JSONResponse function in views.py.
        return Response(serializer.data)
    # If the method is POST...remember, we use POST for creating
    # things on the server.
    elif request.method == u'POST':
        # Create a serializer. Note that we are giving
        # it the data, in JSON format.
        serializer = CollectionSerializer(data=request.DATA)
        # We check if they sent us a valid Collection
        # object.
        if serializer.is_valid():
            # If so, save it to the DB
            serializer.save()
            # Return the object they just sent, along with
            # an appropriate HTTP status code.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If it WASN'T a valid Collection they sent us, return
        # an HTTP error code.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([u'GET', u'POST'])
def labelList(request, format=None):
    '''
    Lists all Labels
    '''
    if request.method == u'GET':
        labels = Label.objects.all()
        serializer = LabelSerializer(labels, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = LabelSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([u'GET', u'PUT', u'DELETE'])
def labelDetail(request, pk=None, ln=None, format=None):
    '''
    Retrieve, update or delete a Label.
    '''
    try:
        if pk is not None:
            label = Label.objects.get(LabelID=pk)
        elif ln is not None:
            label = Label.objects.get(LabelName=ln)
    except Label.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = LabelSerializer(label)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = LabelSerializer(label, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        # If they used DELETE, they want to delete the Collection
        # that they sent the PK for.
        label.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

# @api_view([u'GET', u'POST'])
# def reservationList(request, format=None):
#     '''
#     Retrieve a list of all Reservations
#     '''
#     if request.method == u'GET':
#         reservations = Reservation.objects.all()
#         serializer = ReservationSerializer(reservations, many=True)
#         return Response(serializer.data)
#     elif request.method == u'POST':
#         serializer = ReservationSerializer(data=request.DATA)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([u'GET', u'PUT', u'DELETE'])
def reservationDetail(request, pk, format=None):
    '''
    Retrieve, update or delete a Reservation.
    '''
    try:
        reservation = Reservation.objects.get(ReservationID=pk)
    except Reservation.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == u'GET':
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = ReservationSerializer(reservation, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        reservation.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

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

@api_view([u'GET', u'POST'])
def itemModelList(request):
    if request.method == u'GET':
        all_models = ItemModel.objects.all()
        serializer = ItemModelSerializer(all_models)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = ItemModelSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([u'GET', u'PUT', u'DELETE'])
def itemModelDetail(request, pk=None, mn=None):
    try:
        if pk is not None:
            current_model = ItemModel.objects.get(ModelID=pk)
        elif mn is not None:
            current_model = ItemModel.objects.get(ModelDesignation=mn)
    except ItemModel.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = ItemModelSerializer(current_model)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = ItemModelSerializer(current_model, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        current_model.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view([u'GET', u'POST'])
def itemBrandList(request):
    if request.method == u'GET':
        all_models = ItemBrand.objects.all()
        serializer = ItemBrandSerializer(all_models, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = ItemBrandSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([u'GET', u'PUT', u'DELETE'])
def itemBrandDetail(request, pk=None, bn=None):
    try:
        if pk:
            current_model = ItemBrand.objects.get(BrandID=pk)
        elif bn:
            current_model = ItemBrand.objects.get(BrandName=bn)
    except ItemBrand.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = ItemBrandSerializer(current_model)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = ItemBrandSerializer(current_model, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        current_model.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@api_view([u'GET', u'POST'])
def locationList(request):
    if request.method == u'GET':
        all_models = Location.objects.all()
        serializer = LocationSerializer(all_models, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = LocationSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([u'GET', u'PUT', u'DELETE'])
def locationDetail(request, pk):
    try:
        current_model = Location.objects.get(LocationID=pk)
    except Location.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = LocationSerializer(current_model)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = LocationSerializer(current_model, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        current_model.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


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


@api_view([u'GET', u'POST'])
def actionTypeList(request):
    if request.method == u'GET':
        all_models = ActionType.objects.all()
        serializer = ActionTypeSerializer(all_models, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = ActionTypeSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([u'GET', u'PUT', u'DELETE'])
def actionTypeDetail(request, pk):
    try:
        current_model = ActionType.objects.get(ActionTypeID=pk)
    except ActionType.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = ActionTypeSerializer(current_model)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = ActionTypeSerializer(current_model, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        current_model.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def customerProfileList(request):
    '''
    This function handles retrieving a list of Customer Profiles or
    creating a new one.
    '''
    if request.method == u'GET':
        all_profiles = CustomerProfile.objects.all()
        serializer = CustomerProfileSerializer(all_profiles, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = CustomerProfileSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def customerProfileDetail(request, uid=None):
    '''
    This function handles retrieving details about a single user,
    deleting them or updating them.
    '''
    try:
        currentModel = None
        if uid:
            currentModel = CustomerProfile.objects.get(user__pk=uid)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except CustomerProfile.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        if currentModel:
            serializer = CustomerProfileSerializer(currentModel)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = CustomerProfileSerializer(currentModel, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        currentModel.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def consumableItemList(request):
    '''
    This function handles retrieving a list of consumable items
    or of creating a new one
    '''
    if request.method == u'GET':
        all_items = ConsumableItem.objects.all()
        serializer = ConsumableItemSerializer(all_items, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = ConsumableItemSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([u'GET', u'PUT', u'DELETE'])
def consumableItemDetail(request, pk):
    try:
        current_model = ConsumableItem.objects.get(ItemID=pk)
    except ConsumableItem.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = ConsumableItemSerializer(current_model)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = ConsumableItemSerializer(current_model, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        current_model.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

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


def autocomplete(request):
    '''
    This function takes a search token and a model, and returns autocomplete results to the client.
    '''
    results = []
    if request.GET[u'model'].lower() == u'brand':
        r = ItemBrand.objects.filter(BrandName__icontains = request.GET[u'term'])
        for eachResult in r:
            results.append({u'BrandID':eachResult.BrandID, u'BrandName':eachResult.BrandName})

    elif request.GET[u'model'].lower() == u'model':
        r = ItemModel.objects.filter(ModelDesignation__icontains = request.GET[u'term'])
        for eachResult in r:
            results.append({u'ModelID':eachResult.ModelID, u'ModelDesignation':eachResult.ModelDesignation})

    elif request.GET[u'model'].lower() == u'collection':
        r = Collection.objects.filter(CollectionName__icontains = request.GET[u'term'])
        for eachResult in r:
            results.append({u'CollectionID':eachResult.CollectionID, u'CollectionName': eachResult.CollectionName})

    elif request.GET[u'model'].lower() == u'category':
        r = Label.objects.filter(LabelName__icontains = request.GET[u'term']).exclude(ParentCategory = None)
        for eachResult in r:
            results.append({u'LabelID':eachResult.LabelID, u'LabelName': eachResult.LabelName})

    elif request.GET[u'model'].lower() == u'collection':
        r = Label.objects.filter(CollectionName__icontains = request.GET[u'term'])
        for eachResult in r:
            results.append({u'CollectionID':eachResult.CollectionID, u'CollectionName': eachResult.CollectionName})

    return HttpResponse(json.dumps(results), content_type=u'application/json')


def checkAvailable(item, startTime, endTime):
    actionItems = ActionItem.objects.filter(InventoryItemID=item.pk)
    startDate = datetime.strptime(startTime, "%d-%m-%Y %H:%M:%S")
    endDate = datetime.strptime(endTime, "%d-%m-%Y %H:%M:%S")
    if not actionItem:
        return true
    else:
        actions = Action.objects.filter(ActionID=[x.ActionID for x in actionItems])

        for action in actions:
            actionStartDate = datetime.strptime(action.startTime, "%d-%m-%Y %H:%M:%S")
            actionEndDate = datetime.strptime(action.endTime, "%d-%m-%Y %H:%M:%S")

            if actionStartDate <= startDate and startDate <= actionEndDate:
                return false
            elif actionStartDate <= endDate and endDate <= actionEndDate:
                return false
            elif actionStartDate >= startDate and actionEndDate <= endDate:
                return false
            elif actionStartDate <= startDate and actionEndDate >= endDate:
                return false

        return true


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
