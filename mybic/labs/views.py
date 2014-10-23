import os
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
import sys

from mybic.labs.models import Project,Lab, LabArticle

def labview(request,lab_slug):

    print >>sys.stderr, 'labview! {0}'.format(request.user)

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

    try:
        lab_object = Lab.objects.get(slug=lab_slug)
    except ObjectDoesNotExist:
        return render_to_response('error.html',context_instance=RequestContext(request))

    if lab_object.group in my_groups:
        entries = LabArticle.objects.filter(published=True,lab=lab_object)

        my_projects = Project.objects.filter(
            lab__slug = lab_slug
        )

        context = {'my_groups':my_groups_list,'my_lab':lab_object,'my_projects':my_projects,'entries': entries}

        return render_to_response('projects.html', context, context_instance=RequestContext(request))
    else:
        return render_to_response('error.html',context_instance=RequestContext(request))


def projectview(request,lab_slug,project_slug):
    print >>sys.stderr, 'projectview! {0}'.format(request.user)
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

    lab = Lab.objects.get(slug=lab_slug)
    project = Project.objects.get(slug=project_slug)

    my_projects = Project.objects.filter(
            lab__slug = lab_slug
        )
        
    static_url = settings.STATIC_URL
    project_url = os.path.join(lab_slug,project_slug)
    static_link = os.path.join(static_url,project_url)
    
    context = {'my_groups':my_groups_list,'my_lab':lab,'my_project':project,'my_projects':my_projects,'SLINK':static_link}

    #lab_name = project.lab.name
    if project.public or project.lab.group in my_groups:
        if not project.markdown:
            proj_dir = os.path.join(lab_slug,project_slug,"index.html")
            return render_to_response(proj_dir,context,context_instance=RequestContext(request))
    else:
        return render_to_response('error.html',context_instance=RequestContext(request))
