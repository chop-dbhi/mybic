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
    index_page = models.CharField(default="/mnt/variome/", max_length=300, unique=False, db_index=True,
                                  help_text="full path to your index.html or index.md /mnt/variome/leipzig/liming_err_rnaseq/src/site/_site/index.html or a valid url https://github.research.chop.edu/BiG/pei-err-rna-seq/raw/master/site/index.md or a directory")
    index = models.ForeignKey('ChildIndex',null=True,editable=False)
    static_dir = models.CharField(default="/mnt/variome/", max_length=300, unique=False, db_index=True,
                                  help_text="the directory where your static files are e.g. /mnt/variome/leipzig/err-rna-seq")
    de_dir = models.CharField(max_length=300, unique=False, db_index=True, blank=True, null=True,
                              help_text="data expedition directory")
    lab = models.ForeignKey('Lab')
    git_repo = models.URLField(max_length=300, unique=True, db_index=True,
                               help_text='e.g. http://github.research.chop.edu/cbmi/pcgc')
    git_branch = models.CharField(max_length=100, unique=False, db_index=True, default="master")
    created = models.DateTimeField(default=datetime.now)
    modified = models.DateTimeField(default=datetime.now, auto_now=True)
    public = models.BooleanField(default=False, db_index=True,
                                 help_text='Is this a public project that any myBiC user can see?')
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.slug

    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        url_pattern = re.compile(r"^https?://.+")

        if settings.INDEX_PAGE_HANDLING == 'database':
            try:
                if url_pattern.match(self.index_page):
                    response = urllib2.urlopen(self.index_page)
                    content = response.read()
                else:
                    file = open(self.index_page,'rb')
                    content = file.read()
                #ValueError: Cannot assign "(<ChildIndex: https://github.research.chop.edu/leipzigj/mybic_sandbox/raw/master/README.md>, False)": "Project.index" must be a "ChildIndex" instance.
                self.index, created = ChildIndex.objects.get_or_create(parent=self,page=self.index_page,content=content)
            except OSError, e:
                raise PermissionDenied()

        else:
            # create a symlink to the index file
            # call it lab/project/index.html or lab/project/index.md
            lab_dir = os.path.join(settings.BASE_PATH, 'mybic/labs/templates/', self.lab.slug)
            project_dir = os.path.join(lab_dir, self.slug)
            if not os.path.exists(lab_dir):
                os.mkdir(lab_dir)
            if not os.path.exists(project_dir):
                os.mkdir(project_dir)
            link_name = os.path.join(project_dir, 'index.html')
            try:
                os.unlink(link_name)
            except OSError, e:
                pass

            try:
                if url_pattern.match(self.index_page):
                    response = urllib2.urlopen(self.index_page)
                    fh = open(link_name, "w")
                    fh.write(response.read())
                    fh.close()
                else:
                    os.symlink(self.index_page, link_name)
            except OSError, e:
                raise PermissionDenied()

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
        print >> sys.stderr, 'symlinking {0} to {1}'.format(self.static_dir, project_static)
        try:
            os.symlink(self.static_dir, project_static)
        except OSError, e:
            raise PermissionDenied()
        children = ChildIndex.objects.filter(parent=self)
        for child in children:
            child.save()

        #bump modified date of parent lab
        self.lab.save()

        super(Project, self).save(*args, **kwargs)


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


class ChildIndex(models.Model):
    """ index pages, main and children
        These must be named uniquely from the source (i.e. not index.md)
    """

    class Meta(object):
        verbose_name_plural = "Child Indices"

    parent = models.ForeignKey('Project')
    page = models.CharField(default="/mnt/variome/", max_length=300, unique=False, db_index=True,
                            help_text="full path to your child .html or .md page /mnt/variome/leipzig/liming_err_rnaseq/src/site/_site/additional_info.html or a valid url https://github.research.chop.edu/BiG/pei-err-rna-seq/raw/master/site/additional_info.md")
    content = models.TextField(blank=True, editable=False)

    def __str__(self):
        return self.page

    def __unicode__(self):
        return '%s' % self.page

    def save(self, *args, **kwargs):
        url_pattern = re.compile(r"^https?://.+")

        if settings.INDEX_PAGE_HANDLING == 'database':
            try:
                if url_pattern.match(self.page):
                    response = urllib2.urlopen(self.page)
                    self.content = response.read()
                else:
                    file = open(self.page,'rb')
                    self.content = file.read()
            except OSError, e:
                raise PermissionDenied()

        else:
            # create a symlink to the index file
            lab_dir = os.path.join(settings.BASE_PATH, 'mybic/labs/templates/', self.parent.lab.slug)
            project_dir = os.path.join(lab_dir, self.parent.slug)
            link_name = os.path.join(project_dir, os.path.basename(self.page))
            # if os.path.exists(link_name):
            try:
                os.unlink(link_name)
            except OSError, e:
                pass


            if url_pattern.match(self.page):
                response = urllib2.urlopen(self.page)
                fh = open(link_name, "w")
                fh.write(response.read())
                fh.close()
            else:
                try:
                    os.symlink(self.page, link_name)
                except OSError, e:
                    raise PermissionDenied()

        super(ChildIndex, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # create a symlink to the index file
        lab_dir = os.path.join(settings.BASE_PATH, 'mybic/labs/templates/', self.parent.lab.slug)
        project_dir = os.path.join(lab_dir, self.parent.slug)
        link_name = os.path.join(project_dir, os.path.basename(self.page))
        # if os.path.exists(link_name):
        try:
            os.unlink(link_name)
        except OSError, e:
            pass
        super(ChildIndex, self).delete(*args, **kwargs)


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
