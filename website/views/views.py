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

@csrf_exempt
@api_view([u'GET', u'PUT', u'DELETE'])
def collectionDetail(request, pk, format=None):
    '''
    Retrieve, update or delete a Collection.
    '''
    # We will use try/except. If Django cannot find an object
    # with the primary key we give it using get(), it throws
    # an error.
    try:
        collection = Collection.objects.get(CollectionID=pk)
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
def labelDetail(request, pk, format=None):
    '''
    Retrieve, update or delete a Label.
    '''
    try:
        label = Label.objects.get(LabelID=pk)
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

@api_view([u'GET', u'POST'])
def reservationList(request, format=None):
    '''
    Retrieve a list of all Reservations
    '''
    if request.method == u'GET':
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = ReservationSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    Retrieve, update or delete Label Note.
    '''
    try:
        status = Status.objects.get(StatusID=pk)
    except Status.DoesNotExist:
        return HttpResponse(status=404)

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
        return HttpResponse(status=204)

@api_view([u'GET', u'POST'])
def inventoryItemList(request, format=None):
    '''
    Retrieve a list of all Label Notes
    '''
    if request.method == u'GET':
        inventoryItems = InventoryItem.objects.all()
        serializer = InventoryItemSerializer(inventoryItems, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = InventoryItemSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([u'GET', u'PUT', u'DELETE'])
def inventoryItemDetail(request, pk, format=None):
    '''
    Retrieve, update or delete Inventory Item.
    '''
    try:
        inventoryItem = InventoryItem.objects.get(ItemID=pk)
    except InventoryItem.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == u'GET':
        serializer = InventoryItemSerializer(inventoryItem)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = InventoryItemSerializer(inventoryItem, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        inventoryItem.delete()
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
def itemModelDetail(request, pk):
    try:
        current_model = ItemModel.objects.get(ModelID=pk)
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
def itemBrandDetail(request, pk):
    try:
        current_model = ItemBrand.objects.get(BrandID=pk)
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
        serializer = Location(data=request.DATA)
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




@api_view([u'GET'])
def itemHistoryDetail(request, fk):
    history = InventoryItem.objects.filter(ItemID=fk, order_by=u"ChangeDateTime")
    return HttpResponse(json.dumps(history), status_code=201, content_type=u'application/json')


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

    return HttpResponse(json.dumps(results), content_type=u'application/json')