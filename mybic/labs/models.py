import os
import re
import urllib2
from django.contrib.auth.models import User,Group
from django.db import models
from datetime import datetime
from news.models import Article
from django.conf import settings


class Lab(models.Model):
    """ A lab with a PI
        More than one lab can belong to a group
        A user can belong to more than one group
        So members of that group can access all its labs
    """
    name = models.CharField(max_length=50, unique=True, db_index=True, help_text="lab name only letters, numbers, underscores or hyphens e.g. Pei")
    pi = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    slug = models.SlugField(max_length=50, unique=False, db_index=True, help_text=" only letters, numbers, underscores or hyphens e.g. pei_lab")
        
    def __str__(self):
        return self.slug
    
    def __unicode__(self):
        return '%s' % self.name
    
    def projects(self):
        return Project.objects.filter(lab=self)

class Project(models.Model):
    """ A project with a directory
    """
    name = models.CharField(max_length=50, unique=False, db_index=True, help_text=" display name for this project e.g. 'eRR RNA-Seq Analysis'")
    slug = models.SlugField(max_length=50, unique=False, db_index=True, help_text=" only letters, numbers, underscores or hyphens e.g. err-rna-seq")
    index_page = models.CharField(default="/mnt/variome/",max_length=300, unique=False, db_index=True, help_text="full path to your index.html or index.md /mnt/variome/leipzig/liming_err_rnaseq/src/site/_site/index.html or a valid url https://github.research.chop.edu/BiG/pei-err-rna-seq/raw/master/site/index.md")
    static_dir = models.CharField(default="/mnt/variome/",max_length=300, unique=False, db_index=True, help_text="the directory where your static files are e.g. /mnt/variome/leipzig/err-rna-seq")
    de_dir = models.CharField(max_length=300, unique=False, db_index=True, blank=True, null=True, help_text="data expedition directory")
    lab = models.ForeignKey('Lab')
    git_repo = models.URLField(max_length=300, unique=True, db_index=True, help_text='e.g. http://github.research.chop.edu/cbmi/pcgc')
    git_branch = models.CharField(max_length=100, unique=False, db_index=True, default="master")
    created = models.DateTimeField(default=datetime.now)
    public = models.BooleanField(default=False, db_index=True, help_text='Is this a public project that any myBiC user can see?')

    def __str__(self):
        return self.slug
        
    def __unicode__(self):
        return '%s' % self.name
    
    def save(self):
        #create a symlink to the index file
        #call it lab/project/index.html or lab/project/index.md
        lab_dir = os.path.join(settings.BASE_PATH,'mybic/labs/templates/',self.lab.slug)
        project_dir = os.path.join(lab_dir,self.slug)        
        if not os.path.exists(lab_dir):
            os.mkdir(lab_dir)
        if not os.path.exists(project_dir):
            os.mkdir(project_dir)
        link_name = os.path.join(project_dir,'index.html')
        #if os.path.exists(link_name):
        try:
            os.unlink(link_name)
        except OSError, e:
            pass

        url_pattern = re.compile(r"^https?://.+")
        
        if url_pattern.match(self.index_page):
            response=urllib2.urlopen(self.index_page)
            fh = open(link_name, "w")
            fh.write(response.read())
            fh.close()
        else:
            os.symlink(self.index_page, link_name)
        
        #create a symlink to the static directory on the isilon
        #call it _site/static/lab/project
        lab_static = os.path.join(settings.PROTECTED_ROOT,self.lab.slug)
        project_static = os.path.join(lab_static,self.slug)
        if not os.path.exists(lab_static):
            os.mkdir(lab_static)
        #if os.path.exists(project_static):
        try:
            os.unlink(project_static)
        except OSError, e:
            pass
        os.symlink(self.static_dir, project_static)
        
        super(Project, self).save()
        
class ChildIndex(models.Model):
    """ Additional index pages
        These must be named uniquely from the source (i.e. not index.md)
    """
    
    class Meta(object):
        verbose_name_plural = "Child Indices"
    
    parent = models.ForeignKey('Project')
    page = models.CharField(default="/mnt/variome/",max_length=300, unique=False, db_index=True, help_text="full path to your child .html or .md page /mnt/variome/leipzig/liming_err_rnaseq/src/site/_site/additional_info.html or a valid url https://github.research.chop.edu/BiG/pei-err-rna-seq/raw/master/site/additional_info.md")
    
    def __str__(self):
        return self.page
        
    def __unicode__(self):
        return '%s' % self.page
    
    def save(self):
        #create a symlink to the index file
        lab_dir = os.path.join(settings.BASE_PATH,'mybic/labs/templates/',self.parent.lab.slug)
        project_dir = os.path.join(lab_dir,self.parent.slug)
        link_name = os.path.join(project_dir,os.path.basename(self.page))
        #if os.path.exists(link_name):
        try:
            os.unlink(link_name)
        except OSError, e:
            pass

        url_pattern = re.compile(r"^https?://.+")
    
        if url_pattern.match(self.page):
            response=urllib2.urlopen(self.page)
            fh = open(link_name, "w")
            fh.write(response.read())
            fh.close()
        else:
            os.symlink(self.page, link_name)
    
        super(ChildIndex, self).save()
        
    def delete(self):
        #create a symlink to the index file
        lab_dir = os.path.join(settings.BASE_PATH,'mybic/labs/templates/',self.parent.lab.slug)
        project_dir = os.path.join(lab_dir,self.parent.slug)
        link_name = os.path.join(project_dir,os.path.basename(self.page))
        #if os.path.exists(link_name):
        try:
            os.unlink(link_name)
        except OSError, e:
            pass
        super(ChildIndex, self).delete()
        
class ProjectArticle(Article):
    """ A news item or blog entry associated with a project
    """
    project = models.ForeignKey('Project')

class LabArticle(Article):
    """ A news item or blog entry associated with a lab
    """
    lab = models.ForeignKey('Lab')

class staff(User):
    """ cbmi staff
    """
    projects = models.ManyToManyField(Project)
