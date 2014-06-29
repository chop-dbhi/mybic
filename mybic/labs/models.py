from django.contrib.auth.models import User,Group
from django.db import models
from datetime import datetime

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
    name = models.CharField(max_length=100, unique=True, db_index=True)
    directory = models.CharField(max_length=100, unique=True, db_index=True)
    lab = models.ForeignKey('Lab')
    created = models.DateTimeField(default=datetime.now)

class staff(User):
    """ cbmi staff
    """
    projects = models.ManyToManyField(Project)
