import json
import re

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render

# Auth imports
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login


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
        return HttpResponse(u'Not Implemented')
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
    u = authenticate(username=request.POST['username'], password=request.POST['password'])

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
