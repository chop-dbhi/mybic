import os
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.models import User, Group
import sys
import json
import logging

from mybic.labs.models import Project,ChildIndex,Lab,LabArticle

LOG = logging.getLogger(__package__)

def get_groups(request):
    if request.user.is_staff and not (request.session.get('masquerade',False)):
        print >>sys.stderr, 'admin view'
        my_groups = Group.objects.all()
    else:
        print >>sys.stderr, 'user view'
        my_groups = Group.objects.filter(user=request.user)
    my_groups_list = my_groups.values_list('name', flat=True)
    return my_groups, my_groups_list


def labview(request,lab_slug):

    print >>sys.stderr, 'labview! {0}'.format(request.user)

    if hasattr(request, 'user') and request.user.is_authenticated():
        kwargs = {'user': request.user}
        user = request.user
    else:
        kwargs = {'session_key': request.session.session_key}
        return HttpResponseRedirect(settings.FORCE_SCRIPT_NAME+'/login/')
    
    my_groups, my_groups_list = get_groups(request)
    
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

    my_groups, my_groups_list = get_groups(request)

    try:
        lab = Lab.objects.get(slug=lab_slug)
        project = Project.objects.get(slug=project_slug)
    except ObjectDoesNotExist:
        return render_to_response('error.html',context_instance=RequestContext(request))

    my_projects = Project.objects.filter(
            lab__slug = lab_slug
        )
        
    static_url = settings.PROTECTED_URL
    project_url = os.path.join(lab_slug,project_slug)
    static_link = os.path.join(static_url,project_url)
    
    context = {'my_groups':my_groups_list,'my_lab':lab,'my_project':project,'my_projects':my_projects,'SLINK':static_link}

    if project.public or project.lab.group in my_groups:
        proj_dir = os.path.join(lab_slug,project_slug,"index.html")
        return render_to_response(proj_dir,context,context_instance=RequestContext(request))
    else:
        return render_to_response('error.html',context_instance=RequestContext(request))

def updateproject(request,lab_slug,project_slug):
    print >>sys.stderr, 'updateview! {0}'.format(request.user)
    response_data = {}
    if hasattr(request, 'user') and request.user.is_authenticated():
        kwargs = {'user': request.user}
        user = request.user
    else:
        response_data['result'] = 'failed'
        response_data['message'] = 'Not logged in'

    my_groups, my_groups_list = get_groups(request)

    try:
        lab = Lab.objects.get(slug=lab_slug)
        project = Project.objects.get(slug=project_slug)
    except ObjectDoesNotExist:
        response_data['result'] = 'failed'
        response_data['message'] = 'Project does not exist.'
    
    if project.lab.group in my_groups:
        try:
            project.save()
            children = ChildIndex.objects.filter(parent=project)
            for child in children:
                child.save()
            response_data['result'] = 'success'
            response_data['message'] = 'Project refreshed.'
        except ValidationError:
            response_data['result'] = 'failed'
            response_data['message'] = 'Model data is not validating.'
    else:
        response_data['result'] = 'failed'
        response_data['message'] = 'Project not in your groups.'
    return HttpResponse(json.dumps(response_data), content_type="application/json")



def childview(request,lab_slug,project_slug,child_page):
    print >>sys.stderr, 'childview! {0}'.format(request.user)
    if hasattr(request, 'user') and request.user.is_authenticated():
        kwargs = {'user': request.user}
        user = request.user
    else:
        kwargs = {'session_key': request.session.session_key}
        return HttpResponseRedirect(settings.FORCE_SCRIPT_NAME+'/login/')

    my_groups, my_groups_list = get_groups(request)

    try:
        lab = Lab.objects.get(slug=lab_slug)
        project = Project.objects.get(slug=project_slug)
    except ObjectDoesNotExist:
        return render_to_response('error.html',context_instance=RequestContext(request))

    my_projects = Project.objects.filter(
            lab__slug = lab_slug
        )
        
    static_url = settings.PROTECTED_URL
    project_url = os.path.join(lab_slug,project_slug)
    static_link = os.path.join(static_url,project_url)
    
    context = {'my_groups':my_groups_list,'my_lab':lab,'my_project':project,'my_child':child_page,'my_projects':my_projects,'SLINK':static_link}

    if project.public or project.lab.group in my_groups:
        child_page = os.path.join(lab_slug,project_slug,child_page)
        return render_to_response(child_page,context,context_instance=RequestContext(request))
    else:
        return render_to_response('error.html',context_instance=RequestContext(request))
