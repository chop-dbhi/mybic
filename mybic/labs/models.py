from django.contrib.auth.models import User,Group
from django.db import models
from datetime import datetime
from news.models import Article


class Lab(models.Model):
    """ A lab with a PI
        More than one lab can belong to a group
        A user can belong to more than one group
        So members of that group can access all its labs
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)
    pi = models.ForeignKey(User)
    group = models.ForeignKey(Group)

    def __str__(self):
        return self.name

class Project(models.Model):
    """ A project with a directory
    """
    name = models.CharField(max_length=100, unique=False, db_index=True)
    directory = models.CharField(max_length=100, unique=True, db_index=True, help_text="e.g. err-rna-seq for labs/templates/pei_lab/err-rna-seq")
    index_page = models.CharField(default="index.html",max_length=100, unique=False, db_index=True, help_text="e.g. index.html for labs/templates/pei_lab/err-rna-seq/index.html")
    static_dir = models.CharField(default="",max_length=100, unique=False, db_index=True, help_text="the directory in /home/devuser/webapps/mybic/static/ e.g. /my_lab/my_project/static/")
    #data expedition directory
    de_dir = models.CharField(max_length=100, unique=False, db_index=True, blank=True, help_text="e.g. err-rna-seq for labs/templates/pei_lab/err-rna-seq")
    lab = models.ForeignKey('Lab')
    git_repo = models.CharField(max_length=100, unique=True, db_index=True, help_text='e.g. http://github.research.chop.edu/cbmi/pcgc')
    git_branch = models.CharField(max_length=100, unique=False, db_index=True)
    created = models.DateTimeField(default=datetime.now)
    public = models.BooleanField(default=False, db_index=True, help_text='Is this a public project that any myBiC user can see?')
    markdown = models.BooleanField(default=False, db_index=True, help_text='Is this a markdown page?')
    def __str__(self):
        return self.name


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
