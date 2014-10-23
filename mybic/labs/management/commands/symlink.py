""" Make symlinks for static directories of projects """
from optparse import make_option
import re
import sys
import traceback
from mybic.labs.models import Project,Lab
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'SUBCOMMAND [SUBCOMMAND_ARG]'
    help = ('make symlinks.  Subcommands:\n' +
    '   clear_project- clear symlink in a project\n' +
    '   clear_all - clear all symlinks\n' +
    '   project - make a symlink to project with slug\n' +
    '   all - make all symlinks')
    
def project(self, *args):
    """make a symlink"""
    proj = Project.objects.get(slug=args[0])
    print(proj.name)
    
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