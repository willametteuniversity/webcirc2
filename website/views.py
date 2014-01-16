
# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render

from forms.register import RegistrationForm

def index(request):
    template = loader.get_template('webcirc2.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def registerNewUser(request):
    '''
    This function handles requests relating to registering a new user
    '''

    # This means we need to display the register new user form
    # Let's load the form up
    return render(request, 'forms/register.html', {
    })

def charttest(request):
    template = loader.get_template('charttest.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))