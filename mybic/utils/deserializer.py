from django.core.serializers.python import Deserializer as PythonDeserializer, _get_model
import json
from mybic.labs.models import Project, Lab, ChildIndex
import datetime
import sys
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class ProjectDeserializer():
    # [
    # {
    #     "pk": null,
    #     "model": "labs.project",
    #     "fields": {
    #         "index": null,
    #         "static_dir": "zhangz/projects/falk/2015-01_Worm_Drugs_RNAseq",
    #         "description": null,
    #         "de_dir": "",
    #         "created": null,
    #         "modified": null,
    #         "lab": "falkm",
    #         "public": false,
    #         "index_page": "https://github.research.chop.edu/zhangz/Gas1_Drugs_by_RNAseq/raw/master/index.md",
    #         "git_branch": "master",
    #         "owner": [
    #             "zhangz"
    #         ],
    #         "git_repo": "https://github.research.chop.edu/zhangz/Gas1_Drugs_by_RNAseq",
    #         "autoflank": true,
    #         "slug": "worm_drug_rnaseq",
    #         "name": "Drug effect on Gas1 worm by RNA-seq"
    #     }
    # },
    # {
    #     "pk": null,
    #     "model": "labs.childindex",
    #     "fields": {
    #         "page": "https://github.research.chop.edu/zhangz/Gas1_Drugs_by_RNAseq/raw/master/Gas1_ETOH-vs-Rapamycin.md",
    #         "parent": [
    #             "falkm",
    #             "worm_drug_rnaseq"
    #         ],
    #         "template": null
    #     }
    # }]
    def jsonToProject(self,content):
        # https://djangosnippets.org/snippets/3038/
        #objects = json.load(file_handle)
        objects = json.loads(content)
        for obj in objects:
            # Model = _get_model(obj['model'])
            # if isinstance(obj['pk'], (tuple, list)):
            #     o = Model.objects.get_by_natural_key(*obj['pk'])
            #     obj['pk'] = o.pk

            if obj['model']=='labs.project':
                lab = Lab.objects.get(slug=obj['fields']['lab'])
                obj['fields']['lab'] = lab.id
                owner = User.objects.get(username=obj['fields']['owner'])
                obj['fields']['owner'] = owner.id
                if 'created' in obj['fields']:
                    if obj['fields']['created'] == None or obj['fields']['created'] == '':
                        obj['fields']['created'] = datetime.datetime.today()
                if 'modified' in obj['fields']:
                    obj['fields']['modified'] = datetime.datetime.today()
            elif obj['model']=='labs.childindex':
                pass
        with transaction.atomic():
            try:
                for obj in objects:
                    if obj['model']=='labs.childindex':
                        print >> sys.stderr, 'childindex obj'
                        (labslug, projectslug) = obj['fields']['parent']
                        obj['fields']['parent'] = Project.objects.get(lab__slug=labslug, slug=projectslug).id
                    for desobj in PythonDeserializer([obj]):
                        # for some reason this deserializedobject calls save on the Model baseclass directly
                        if desobj.object.__class__.__name__ == 'Project':
                            print >> sys.stderr, 'project!'
                            # does this project exist?
                            try:
                                projectslug = obj['fields']['slug']
                                # lab id gets set above
                                lab_id = obj['fields']['lab']
                                old_project = Project.objects.get(lab=lab_id, slug=projectslug)
                                old_project.delete()
                            except ObjectDoesNotExist:
                                pass
                            desobj.save()
                            createdProject = Project.objects.get(id=desobj.object.pk)
                            createdProject.save()
                        elif desobj.object.__class__.__name__ == 'ChildIndex':
                            print >> sys.stderr, 'desobj! {0}'.format(desobj.object.parent)
                            desobj.save()
                            createdIndex = ChildIndex.objects.get(id=desobj.object.pk)
                            createdIndex.save()
                        else:
                            raise Exception('object type unknown')
            except Exception as e:
                print e
        return (createdProject.lab.slug,createdProject.slug)