from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from optparse import make_option
from django.conf import settings
from django.db import transaction

from mybic.labs.models import Project

class Command(BaseCommand):
    """ Walks project directories, including static directories and children
    """
    args = ''
    help = ('Refresh projects')

    option_list = BaseCommand.option_list + \
                  (
                      make_option('--project',
                                  dest='project',
                                  default=None,
                                  metavar='NAME',
                                  help='Specify project slug name'),
                  )

    def handle(self, *args, **options):
        """ Handle the command line """
        if options['project']:
            try:
                myproject = Project.objects.get(slug=options['project'])
                myproject.save()
            except ObjectDoesNotExist:
                fmt = 'Project matching slug={slug} not found'
                print(fmt.format(slug=options['project']))
        else:
            for myproject in Project.objects.all().order_by('modified'):
                myproject.save()