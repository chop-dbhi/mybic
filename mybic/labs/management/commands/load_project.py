from django.core.management.base import BaseCommand
import json
from mybic.labs.models import Project, Lab
from django.core.serializers.python import Deserializer as PythonDeserializer, _get_model
from mybic.utils.deserializer import ProjectDeserializer
#from django.core import serializers
import sys
from django.utils import six
from django.core.serializers.base import DeserializationError

class Command(BaseCommand):
    """ Load a project from JSON
    """

    args = ''
    help = ('Deserialize a json file into a project')

    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        """ Handle the command line """
        if len(args):
            filename = args[0]
        else:
            print self.help
            sys.exit(0)
 
        file_handle = open(filename)
        content = file_handle.read()
        my_deserializer = ProjectDeserializer()
        my_deserializer.jsonToProject(content)