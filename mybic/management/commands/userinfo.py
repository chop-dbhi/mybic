from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from mybic.labs.models import Lab
import sys, traceback

from optparse import make_option

class Command(BaseCommand):
    args = 'SUBCOMMAND [SUBCOMMAND_ARG]'

    help = ('Displays info about user.  Subcommands:\n' +
             '   directory - get a list of groups, labs, and users\n'
            )
    def directory(self, *args):
        for group in Group.objects.all().order_by('name'):
            print group
            print "\tLabs:"
            for lab in Lab.objects.filter(group=group).order_by('slug'):
                print "\t\t{0} PI: {1} {2} ({3}) <{4}>".format(lab.name,lab.pi.first_name,lab.pi.last_name, lab.pi.username, lab.pi.email)
            print "\tPeople:"
            for person in group.user_set.all().order_by('last_name'):
                print "\t\t{0} {1} ({2}) <{3}>".format(person.first_name,person.last_name,person.username, person.email)

    def handle(self, *args, **options):
        """ Handle the command line """

        self.options = options   # pylint: disable=W0201

        # Do subcommand
        if len(args):
            subcommand = args[0]
        else:
            print self.help
            return

        functions = {
            'directory': self.directory
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
