import os
import re
import urllib2
import sys
from django.contrib.auth.models import User, Group
from django.db import models
from datetime import datetime
from news.models import Article
from django.conf import settings
from django.core.exceptions import PermissionDenied

from dbtemplates.models import Template

class Lab(models.Model):
    """ A lab with a PI
        More than one lab can belong to a group
        A user can belong to more than one group
        So members of that group can access all its labs
    """
    name = models.CharField(max_length=50, unique=True, db_index=True,
                            help_text="lab name only letters, numbers, underscores or hyphens e.g. Pei")
    pi = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    slug = models.SlugField(max_length=50, unique=False, db_index=True,
                            help_text=" only letters, numbers, underscores or hyphens e.g. pei_lab")
    modified = models.DateTimeField(default=datetime.now, auto_now=True)

    def __str__(self):
        return self.slug

    def __unicode__(self):
        return '%s' % self.name

    def projects(self):
        return Project.objects.filter(lab=self).order_by('-modified')


class Project(models.Model):
    """ A project with a directory
    """
    name = models.CharField(max_length=50, unique=False, db_index=True,
                            help_text=" display name for this project e.g. 'eRR RNA-Seq Analysis'")
    description = models.TextField(unique=False, db_index=True, null=True, help_text="description of the project")
    slug = models.SlugField(max_length=50, unique=False, db_index=True,
                            help_text=" only letters, numbers, underscores or hyphens e.g. err-rna-seq")
    index_page = models.CharField(default="", max_length=300, unique=False, db_index=True,
                                  help_text="path to your index.html or index.md on the Isilon mount e.g. leipzig/liming_err_rnaseq/src/site/_site/index.html or a valid url https://github.research.chop.edu/BiG/pei-err-rna-seq/raw/master/site/index.md or a directory")
    index = models.ForeignKey('ChildIndex',null=True,editable=False,on_delete=models.SET_NULL)
    static_dir = models.CharField(default="", max_length=300, unique=False, db_index=True,
                                  help_text="Isilon subdirectory where your static files are e.g. leipzig/err-rna-seq")
    de_dir = models.CharField(max_length=300, unique=False, db_index=True, blank=True, null=True,
                              help_text="data expedition directory", editable=False)
    lab = models.ForeignKey('Lab')
    git_repo = models.URLField(max_length=300, unique=True, db_index=True,
                               help_text='e.g. http://github.research.chop.edu/cbmi/pcgc')
    git_branch = models.CharField(max_length=100, unique=False, db_index=True, default="master")
    created = models.DateTimeField(default=datetime.now)
    modified = models.DateTimeField(default=datetime.now, auto_now=True)
    public = models.BooleanField(default=False, db_index=True,
                                 help_text='Is this a public project that any myBiC user can see?')
    owner = models.ForeignKey(User, help_text="Set this to the analyst responsible for maintaining the content. This person will receive emails for broken links, etc.")
    autoflank = models.BooleanField(default=settings.AUTOFLANK, help_text="Automatically flank all index pages with base template tags and .md files with markdown template tags")

    def __str__(self):
        return self.slug

    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):


        # create a symlink to the static directory on the isilon
        #call it _site/static/lab/project
        lab_static = os.path.join(settings.PROTECTED_ROOT, self.lab.slug)
        project_static = os.path.join(lab_static, self.slug)
        if not os.path.exists(lab_static):
            os.mkdir(lab_static)
        try:
            print >> sys.stderr, 'unlking! {0}'.format(project_static)
            os.unlink(project_static)
        except OSError, e:
            pass
        print >> sys.stderr, 'symlinking {0} to {1}'.format(os.path.join(settings.ISILON_ROOT,self.static_dir), project_static)
        try:
            os.symlink(os.path.join(settings.ISILON_ROOT,self.static_dir), project_static)
        except OSError, e:
            raise PermissionDenied()

        #bump modified date of parent lab
        self.lab.save()

        super(Project, self).save(*args, **kwargs)

        self.index, created = ChildIndex.objects.get_or_create(parent=self,page=self.index_page)

        children = ChildIndex.objects.filter(parent=self)
        for child in children:
            child.save()






class ChildIndex(models.Model):
    """ index pages, main and children
        These must be named uniquely from the source (i.e. not index.md)
    """

    class Meta(object):
        verbose_name_plural = "Child Indices"

    parent = models.ForeignKey('Project')
    page = models.CharField(default="", max_length=300, unique=False, db_index=True,
                            help_text="Path to your child .html or .md page on the Isilon mount leipzig/liming_err_rnaseq/src/site/_site/additional_info.html or a valid url https://github.research.chop.edu/BiG/pei-err-rna-seq/raw/master/site/additional_info.md")
    template = models.ForeignKey(Template, null=True, editable=False, on_delete=models.SET_NULL)

    def __str__(self):
        return self.page

    def __unicode__(self):
        return '%s' % self.page

    def save(self, *args, **kwargs):
        url_pattern = re.compile(r"^https?://.+")


        if url_pattern.match(self.page):
            response = urllib2.urlopen(self.page)
            pre_content = response.read()
        else:
            print "trying to open {0} {1}".format(settings.ISILON_ROOT, os.path.join(settings.ISILON_ROOT,self.page))
            file = open(os.path.join(settings.ISILON_ROOT,self.page),'rb')
            pre_content = file.read()

        if self.parent.autoflank == True:
            if self.page.lower().endswith('.md'):
                open_flank = '{% extends "base.html" %} {% load markdown_tags %} {% block content %} {% markdown %}'
                close_flank = '{% endmarkdown %} {% endblock %}'
            else:
                open_flank = '{% extends "base.html" %} {% block content %}'
                close_flank = '{% endblock %}'
            # clear out any existing tags that would interfere, including legacy tags
            # flank with new tags
            content = "{0}\n{1}\n{2}\n".format(open_flank,
                pre_content.replace('{% extends "base.html" %}', '').
                            replace('{% load markdown_tags %}','').
                            replace('{% load markdown_deux_tags %}','').
                            replace('{% block content %}', '').
                            replace('{% endblock %}', '').
                            replace('{% markdown %}', '').
                            replace('{% endmarkdown %}', ''),
                close_flank)
        else:
            content=pre_content
        if settings.INDEX_PAGE_HANDLING == 'database':
            try:
                self.template.delete()
            except:
                pass
            self.template = Template.objects.create(name=os.path.join(self.parent.lab.slug,self.parent.slug,os.path.basename(self.page)),content=content)
        else:
            # create a symlink to the index file
            lab_dir = os.path.join(settings.BASE_PATH, 'mybic/labs/templates/', self.parent.lab.slug)
            project_dir = os.path.join(lab_dir, self.parent.slug)
            link_name = os.path.join(project_dir, os.path.basename(self.page))
            try:
                os.unlink(link_name)
            except OSError, e:
                pass

            # web sources are always copied, files can be symlinked
            try:
                if settings.INDEX_PAGE_HANDLING == 'symlink' and not url_pattern.match(self.page):
                    os.symlink(os.path.join(settings.ISILON_ROOT,self.page), link_name)
                else:
                    fh = open(link_name, "w")
                    fh.write(content)
                    fh.close()
            except OSError, e:
                raise PermissionDenied()
        super(ChildIndex, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        lab_dir = os.path.join(settings.BASE_PATH, 'mybic/labs/templates/', self.parent.lab.slug)
        project_dir = os.path.join(lab_dir, self.parent.slug)
        link_name = os.path.join(project_dir, os.path.basename(self.page))
        # if os.path.exists(link_name):
        try:
            os.unlink(link_name)
        except OSError, e:
            pass
        super(ChildIndex, self).delete(*args, **kwargs)

class ProjectFile(models.Model):
    """ Holds record of template files to be extracted by solr
    """
    project = models.ForeignKey(Project)
    filepath = models.CharField(max_length=500, unique=False, db_index=True)

class ProtectedFile(models.Model):
    """ Holds record of protected files to be extracted by solr
    """
    project = models.ForeignKey(Project)
    filepath = models.CharField(max_length=500, unique=False, db_index=True)

class ProjectArticle(Article):
    """ A news item or blog entry associated with a project
    """
    project = models.ForeignKey('Project')


class LabArticle(Article):
    """ A news item or blog entry associated with a lab
    """
    lab = models.ForeignKey('Lab')


class SiteArticle(Article):
    """ A news item or blog entry for everyone
    """


class staff(User):
    """ cbmi staff
    """
    projects = models.ManyToManyField(Project)
