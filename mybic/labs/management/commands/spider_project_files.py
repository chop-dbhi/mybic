from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from optparse import make_option
from django.conf import settings
from django.db import transaction
import os

from mybic.labs.models import Project,ProjectFile

class Walker(object):
    def clear_project(self,project):
        proj_files = ProjectFile.objects.filter(project=project)
        for proj_file in proj_files:
            proj_file.delete()

    def walk_project(self, project):
        for root, dirs, files in os.walk(os.path.join(settings.PROJECT_ROOT,project.slug)):
            for file in files:
                if file.endswith('.txt'):
                    print file

    def do_project(self,project):
        with transaction.atomic():
            self.clear_project(project)
            self.walk_project(project)


class Command(BaseCommand):
    """ Walks project directories, including static directories and children
    """
    args = ''
    help = ('Walks project directories, including static directories and children')

    option_list = BaseCommand.option_list + \
        (
            make_option('--project',
                        dest='project',
                        default='default',
                        metavar='NAME',
                        help='Specify project slug name'),
        )

    def handle(self, *args, **options):
        """ Handle the command line """
        walker = Walker()
        if options['project']:
            try:
                myproject = Project.objects.get(slug=options['project'])
            except ObjectDoesNotExist:
                fmt = 'Project matching slug={slug} not found'
                raise ObjectDoesNotExist(fmt.format(slug=options['project']))
            walker.do_project(myproject)
        else:
            for myproject in Project.objects.all():
                walker.do_project(myproject)