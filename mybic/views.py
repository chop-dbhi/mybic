from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template import RequestContext
import sys

from mybic.labs.models import Lab
from django.contrib.auth.models import User,Group

def dashboard(request):
    print >>sys.stderr, 'dashboard!'
    if hasattr(request, 'user') and request.user.is_authenticated():
        kwargs = {'user': request.user}
    else:
        kwargs = {'session_key': request.session.session_key}
        return HttpResponseRedirect(settings.FORCE_SCRIPT_NAME+'/login/')

    my_groups = request.user.groups.values_list('name',flat=True)

    my_labs = Lab.objects.filter(
        group__in = request.user.groups.all()
    ).values_list('name',flat=True)

    context = {'my_groups':my_groups,'my_labs':my_labs}


    return render_to_response('dashboard.html', context, context_instance=RequestContext(request))