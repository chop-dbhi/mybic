from django.core.serializers.python import Deserializer as PythonDeserializer, _get_model
import json
from mybic.labs.models import Project, Lab
import datetime

class ProjectDeserializer():
    def jsonToProject(self,content):
        # https://djangosnippets.org/snippets/3038/
        #objects = json.load(file_handle)
        objects = json.loads(content)
        for obj in objects:
            Model = _get_model(obj['model'])
            if isinstance(obj['pk'], (tuple, list)):
                o = Model.objects.get_by_natural_key(*obj['pk'])
                obj['pk'] = o.pk
            lab = Lab.objects.get(slug=obj['fields']['lab'])
            obj['fields']['lab'] = lab.id
            if obj['fields']['created'] == None or obj['fields']['created'] == '':
                obj['fields']['created'] = datetime.datetime.today()
            obj['fields']['modified'] = datetime.datetime.today()
        try:
            for obj in PythonDeserializer(objects):
                # for some reason this deserializedobject calls save on the Model baseclass directly
                obj.save()
                createdProject = Project.objects.get(id=obj.object.pk)
                createdProject.save()
        except Exception as e:
            print e