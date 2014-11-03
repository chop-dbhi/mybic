from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import sys
import os

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
        my_groups_list = my_groups.values_list('name', flat=True)
    else:
        my_groups = Group.objects.filter(user=request.user)
        my_groups_list = my_groups.values_list('name',flat=True)
        
    my_labs = Lab.objects.filter(
        group__in = my_groups
    )

    my_projects = Project.objects.filter(
            lab__name__in = my_labs.values_list('name',flat=True)
        ).values('slug')

    context = {'my_groups':my_groups_list,'my_labs':my_labs,'my_projects':my_projects}


    return render_to_response('dashboard.html', context, context_instance=RequestContext(request))

#http://glitterbug.in/blog/serving-protected-files-from-nginx-with-django-11/show/
def protected_file(request,lab,project,path):
    print >>sys.stderr, 'protectedfile! {0} {1} {2} {3}'.format(request.user,lab, project,path)
    response = HttpResponse()
    debug=False
    if debug:
        response['X-Accel-Redirect'] = 'test'
    else:
        if hasattr(request, 'user') and request.user.is_authenticated():
            kwargs = {'user': request.user}
            user = request.user
            if user.is_staff:
                my_groups = Group.objects.all()
                my_groups_list = my_groups.values_list('name', flat=True)
            else:
                my_groups = Group.objects.filter(user=request.user)
                my_groups_list = my_groups.values_list('name',flat=True)

            try:
                lab_object = Lab.objects.get(slug=lab)
                project_object = Project.objects.get(slug=project)
            except ObjectDoesNotExist:
                raise Http404
            if lab_object.group in my_groups:
                if path.endswith("pdf"):
                    response['Content-Type'] = 'application/pdf'
                elif path.endswith("xlsx"):
                    print >>sys.stderr,"xslx file!\n"
                    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.basename(path))
                elif path.endswith("xls"):
                    print >>sys.stderr,"xls file!\n"
                    response['Content-Type'] = 'application/vnd.ms-excel'
                    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.basename(path))
                else:
                    print >>sys.stderr,"some other file!\n"
                response['X-Accel-Redirect'] = '{0}/{1}/{2}/{3}'.format('/protected/', lab, project, path)
            else:
                return render_to_response('error.html',context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(settings.FORCE_SCRIPT_NAME+'/login/')
    return response
