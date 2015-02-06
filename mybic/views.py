from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
import sys
import os
import mimetypes
from news.models import Article
import json
import logging

from mybic.labs.models import Lab, Project, SiteArticle
from django.contrib.auth.models import User, Group


def get_groups(request):
    if request.user.is_staff and not (request.session.get('masquerade', False)):
        print >> sys.stderr, 'admin view'
        my_groups = Group.objects.all()
    else:
        print >> sys.stderr, 'user view'
        my_groups = Group.objects.filter(user=request.user)

    return my_groups


def get_dash_context(request):
    my_groups = get_groups(request)
    my_groups_list = my_groups.values_list('name', flat=True)
    my_labs = Lab.objects.filter(
        group__in=my_groups
    ).order_by('-modified')

    my_projects = Project.objects.filter(
        lab__name__in=my_labs.values_list('name', flat=True)
    ).values('slug').order_by('-modified')

    entries = SiteArticle.objects.filter(published=True)

    context = {'my_groups': my_groups_list, 'my_labs': my_labs, 'my_projects': my_projects, 'entries': entries}
    return context


def dashboard(request):
    print >> sys.stderr, 'dashboard! {0} session {1}'.format(request.user, request.session._session_key)

    if hasattr(request, 'user') and request.user.is_authenticated():
        kwargs = {'user': request.user}
        user = request.user
    else:
        kwargs = {'session_key': request.session.session_key}
        return HttpResponseRedirect(settings.FORCE_SCRIPT_NAME + '/login/')

    if 'count' in request.session:
        request.session['count'] += 1
        print >> sys.stderr, 'count {0}'.format(request.session['count'])
    else:
        request.session['count'] = 1
        print >> sys.stderr, 'No count in session. Setting to 1'

    masquerade = request.session.get('masquerade', None)
    print >> sys.stderr, 'masquerade {0}'.format(masquerade)

    context = get_dash_context(request)

    return render_to_response('dashboard.html', context, context_instance=RequestContext(request))


def masquerade(request):
    """ Toggles the masquerade setting allowing admins to pretend to be users
    """
    print >> sys.stderr, 'toggleview!'
    response_data = {}
    try:
        # if its not set or its false this condition will be false
        if not (request.session.get('masquerade', False)):
            request.session['masquerade'] = True
        else:
            request.session['masquerade'] = False
    except Exception, e:
        request.session['masquerade'] = True
    request.session.modified = True
    print >> sys.stderr, 'toggling to masquerade:{0}'.format(request.session['masquerade'])

    context = get_dash_context(request)

    return render_to_response('dashboard.html', context, context_instance=RequestContext(request))


# http://glitterbug.in/blog/serving-protected-files-from-nginx-with-django-11/show/
def protected_file(request, lab, project, path):
    print >> sys.stderr, 'protectedfile! {0} {1} {2} {3}'.format(request.user, lab, project, path)
    LOG = logging.getLogger("protected_file")

    response = HttpResponse()
    debug = False
    if debug:
        response['X-Accel-Redirect'] = 'test'
    else:
        if hasattr(request, 'user') and request.user.is_authenticated():
            kwargs = {'user': request.user}
            user = request.user
            if user.is_staff and not (
                    request.session and request.session.get('masquerade') and request.session.masquerade == True):
                my_groups = Group.objects.all()
                my_groups_list = my_groups.values_list('name', flat=True)
            else:
                my_groups = Group.objects.filter(user=request.user)
                my_groups_list = my_groups.values_list('name', flat=True)

            try:
                lab_object = Lab.objects.get(slug=lab)
                project_object = Project.objects.get(slug=project)
            except ObjectDoesNotExist:
                raise Http404
            if lab_object.group in my_groups:
                file_location = os.path.join(settings.PROTECTED_ROOT, lab, project, path)
                if not os.path.exists(file_location):
                    # TODO: there must be a better way to pass this
                    pro_path_json = json.dumps({'project': project_object.id, 'path': path})
                    LOG.error(pro_path_json)
                    raise Http404
                if path.endswith("pdf"):
                    response['Content-Type'] = 'application/pdf'
                elif path.endswith("xlsx"):
                    print >> sys.stderr, "xslx file!\n"
                    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.basename(path))
                elif path.endswith("png"):
                    response['Content-Type'] = 'image/png'
                elif path.endswith("jpeg") or path.endswith("jpg"):
                    response['Content-Type'] = 'image/jpeg'
                elif path.endswith("xls"):
                    print >> sys.stderr, "xls file!\n"
                    response['Content-Type'] = 'application/vnd.ms-excel'
                    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.basename(path))
                elif path.endswith("html") or path.endswith("htm") or path.endswith("txt"):
                    response['Content-Type'] = 'text/html'
                elif path.endswith("svg"):
                    response['Content-Type'] = 'image/svg+xml'
                else:
                    print >> sys.stderr, "some other file!\n"
                    mime = mimetypes.guess_type(os.path.basename(path))[0] or 'application/octet-stream'
                    response['Content-Type'] = mime
                    print >> sys.stderr, "format guess: {0}".format(mime)
                    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.basename(path))
                response['X-Accel-Redirect'] = '{0}/{1}/{2}/{3}'.format('/protected/', lab, project, path)
            else:
                return render_to_response('error.html', context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(settings.FORCE_SCRIPT_NAME + '/login/')
    return response


def news(request):
    entries = Article.objects.filter(published=True)
    return render(request, 'news/list.html', {
        'entries': entries,
    })
