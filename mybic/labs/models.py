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
    name = models.CharField(max_length=50, unique=True, db_index=True, help_text="lab name only letters, numbers, underscores or hyphens e.g. Pei")
    pi = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    slug = models.SlugField(max_length=50, unique=False, db_index=True, help_text=" only letters, numbers, underscores or hyphens e.g. pei_lab")
        
    def __str__(self):
        return self.slug
    
    def __unicode__(self):
        return '%s' % self.name

class Project(models.Model):
    """ A project with a directory
    """
    name = models.CharField(max_length=50, unique=False, db_index=True, help_text=" display name for this project e.g. 'eRR RNA-Seq Analysis'")
    slug = models.SlugField(max_length=50, unique=False, db_index=True, help_text=" only letters, numbers, underscores or hyphens e.g. err-rna-seq")
    index_page = models.FilePathField(default="/mnt/variome/me/lab/project/site/index.html",max_length=300, unique=False, db_index=True, help_text="full path to your index.html /mnt/variome/leipzig/liming_err_rnaseq/src/site/_site/index.html")
    static_dir = models.FilePathField(default="",max_length=300, unique=False, db_index=True, help_text="the directory where your static files are e.g. /mnt/variome/leipzig/err-rna-seq")
    #data expedition directory
    de_dir = models.CharField(max_length=300, unique=False, db_index=True, blank=True, null=True, help_text="e.g. err-rna-seq for labs/templates/pei_lab/err-rna-seq")
    lab = models.ForeignKey('Lab')
    git_repo = models.URLField(max_length=300, unique=True, db_index=True, help_text='e.g. http://github.research.chop.edu/cbmi/pcgc')
    git_branch = models.CharField(max_length=100, unique=False, db_index=True, default="master")
    created = models.DateTimeField(default=datetime.now)
    public = models.BooleanField(default=False, db_index=True, help_text='Is this a public project that any myBiC user can see?')
    markdown = models.BooleanField(default=False, db_index=True, help_text='Is this a markdown page?')

    def __str__(self):
        return self.slug
        
    def __unicode__(self):
        return '%s' % self.name
    
    def save(self):        
        if not os.path.exists(lab.slug):
            os.path.join(lab_dir)
        if not os.path.exists(project_dir):
            os.mkdir(project_dir)
        os.symlink(proj.index_page, link_name)
        super(Base, self).save()


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
