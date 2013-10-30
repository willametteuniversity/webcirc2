# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render

def index(request):
    template = loader.get_template('webcirc2.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def charttest(request):
    template = loader.get_template('charttest.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))