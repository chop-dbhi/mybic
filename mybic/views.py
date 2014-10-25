from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template import RequestContext
import sys

from mybic.labs.models import Lab, Project
from django.contrib.auth.models import User,Group

def dashboard(request):
    print >>sys.stderr, 'dashboard! {0}'.format(request.user)
    if hasattr(request, 'user') and request.user.is_authenticated():
        kwargs = {'user': request.user}
        user = request.user
    else:
        kwargs = {'session_key': request.session.session_key}
        return HttpResponseRedirect(settings.FORCE_SCRIPT_NAME+'/login/')

    if user.is_staff:
        my_groups = Group.objects.all()
        my_groups_list = Group.objects.values_list('name', flat=True)
    else:
        my_groups = request.user.groups.all()
        my_groups_list = request.user.groups.values_list('name',flat=True)
        
    my_labs = Lab.objects.filter(
        group__in = my_groups
    )

    my_projects = Project.objects.filter(
            lab__name__in = my_labs.values_list('name',flat=True)
        ).values('slug')

    context = {'my_groups':my_groups_list,'my_labs':my_labs,'my_projects':my_projects}


    return render_to_response('dashboard.html', context, context_instance=RequestContext(request))

#http://glitterbug.in/blog/serving-protected-files-from-nginx-with-django-11/show/
def protected_file(request,path):
    print >>sys.stderr, 'protectedfile! {0} {1}'.format(request.user,path)
    if hasattr(request, 'user') and request.user.is_authenticated():
        kwargs = {'user': request.user}
        user = request.user
    else:
        kwargs = {'session_key': request.session.session_key}
        return HttpResponseRedirect(settings.FORCE_SCRIPT_NAME+'/login/')
    response = HttpResponse()
    response['X-Accel-Redirect'] = '%s/%s' % (settings.FORCE_SCRIPT_NAME, path)
    #response['X-Accel-Redirect'] = '/protected/pei_lab/err_rna_seq/diffExp.pdf'
    return response
