# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
def charttest(request):
    template = loader.get_template('charttest.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))