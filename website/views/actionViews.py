from django.http import HttpResponse
from django.template import RequestContext, loader

def viewTodaysActions(request):
    template = loader.get_template(u'todays_actions.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))