import os
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
import sys

from mybic.labs.models import Project,Lab, LabArticle

def labview(request,lab_name):
    my_groups = request.user.groups.values_list('name',flat=True)

    try:
        lab_object = Lab.objects.get(name=lab_name)
    except ObjectDoesNotExist:
        return render_to_response('error.html',context_instance=RequestContext(request))

    if lab_object.group in request.user.groups.all():
        entries = LabArticle.objects.filter(published=True,lab=lab_object)

        my_projects = Project.objects.filter(
            lab__name = lab_name
        ).values_list('slug',flat=True)

        context = {'my_groups':my_groups,'my_lab':lab_name,'my_projects':my_projects,'entries': entries}

        return render_to_response('projects.html', context, context_instance=RequestContext(request))
    else:
        return render_to_response('error.html',context_instance=RequestContext(request))

def projectview(request,lab_name,project_slug):
    my_groups = request.user.groups.values_list('name',flat=True)

    project = Project.objects.get(slug=project_slug)

    my_projects = Project.objects.filter(
            lab__name = lab_name
        ).values_list('slug',flat=True)

    context = {'my_groups':my_groups,'my_lab':lab_name,'my_project':project_slug,'my_projects':my_projects}

    #lab_name = project.lab.name
    if project.public or project.lab.group in request.user.groups.all():
        proj_dir = os.path.join(lab_name,project.directory,project.index_page)
        return render_to_response(proj_dir,context,context_instance=RequestContext(request))
    else:
        return render_to_response('error.html',context_instance=RequestContext(request))
