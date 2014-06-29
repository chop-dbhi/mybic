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

class Project(models.Model):
    """ A project with a directory
    """
    name = models.CharField(max_length=100, unique=False, db_index=True)
    directory = models.CharField(max_length=100, unique=True, db_index=True)
    #data expedition directory
    de_dir = models.CharField(max_length=100, unique=True, db_index=True, null=True)
    lab = models.ForeignKey('Lab')
    git_repo = models.CharField(max_length=100, unique=True, db_index=True)
    git_branch = models.CharField(max_length=100, unique=False, db_index=True)
    created = models.DateTimeField(default=datetime.now)

class ProjectArticle(Article):
    """ A news item or blog entry associated with a project
    """
    project = models.ForeignKey('Project')

class staff(User):
    """ cbmi staff
    """
    projects = models.ManyToManyField(Project)
