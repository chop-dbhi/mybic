from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template import RequestContext

def index(request):
    if hasattr(request, 'user') and request.user.is_authenticated():
        kwargs = {'user': request.user}
    else:
        kwargs = {'session_key': request.session.session_key}
        return HttpResponseRedirect(settings.FORCE_SCRIPT_NAME+'/login/')

    context = {'lab':request.lab}

    return render_to_response('dashboard.html', context, context_instance=RequestContext(request))

def projects(request,lab):
    if hasattr(request, 'user') and request.user.is_authenticated():
        kwargs = {'user': request.user}
    else:
        kwargs = {'session_key': request.session.session_key}
        return HttpResponseRedirect(settings.FORCE_SCRIPT_NAME+'/login/')

    context = {'lab':lab}

    return render_to_response('projects.html', context, context_instance=RequestContext(request))