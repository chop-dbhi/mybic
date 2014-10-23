""" Make symlinks for static directories of projects """
from optparse import make_option
import re
import sys
import traceback
from mybic.labs.models import Project,Lab
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'SUBCOMMAND [SUBCOMMAND_ARG]'
    help = ('make symlinks.  Subcommands:\n' +
    '   clear_project- clear symlink in a project\n' +
    '   clear_all - clear all symlinks\n' +
    '   project - make a symlink to project with lab_slug project_slug\n' +
    '   all - make all symlinks')
    
    def project(self, *args):
        """make a symlink"""
        try:
            lab = Lab.objects.get(slug=args[0])
            proj = Project.objects.get(lab=lab,slug=args[1])
        
            static_url = settings.STATIC_URL
            project_url = os.path.join(args[0],args[1])
            static_link = os.path.join(static_url,project_url)
        
            print "symlinking %s %s".format(proj.static_dir)
        except Exception as e:
            traceback.print_tb(sys.exc_traceback)
            msg = 'Error running manifestmd5 {subcmd}: {exc}'
            raise CommandError(msg.format(subcmd=subcommand, exc=str(e)))
    
    def create_template(self,*args):
        ""Create a template in lab called project""
        try:
            lab = Lab.objects.get(slug=args[0])
            proj = Project.objects.get(lab=lab,slug=args[1])
            
            if not os.path.exists(proj.index_page):
                raise Exception("This index file {0} does not exist".proj.index_page)
            lab_dir = os.path.join(BASE_PATH,'mybic/labs/templates/',lab.slug)
            project_dir = os.path.join(BASE_PATH,'mybic/labs/templates/',lab.slug,proj.slug)
            if not os.path.exists(lab.slug):
                os.path.join(lab_dir)
            if not os.path.exists(project_dir):
                os.mkdir(project_dir)
            
            os.symlink(proj.index_page, link_name)
            
        
    def handle(self, *args, **options):
        """ Handle the command line """

        self.options = options

        # Do subcommand
        if len(args):
            subcommand = args[0]
        else:
            print self.help
            return

        functions = {
            'project': self.project
        }
        if subcommand not in functions:
            raise CommandError("Invalid subcommand '%s'" % subcommand)
        rest = args[1:]
        try:
            functions[subcommand](*rest)
        except Exception as e:
            traceback.print_tb(sys.exc_traceback)
            msg = 'Error running manifestmd5 {subcmd}: {exc}'
            raise CommandError(msg.format(subcmd=subcommand, exc=str(e)))