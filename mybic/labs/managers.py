from django.db import models

class ProjectManager(models.Manager):
    def get_by_natural_key(self, labslug, slug):
        return self.get(lab_slug=labslug,slug=slug)

class ChildIndexManager(models.Manager):
    def get_by_natural_key(self, page, labslug, slug):
        return self.get(page=page, parent__lab__slug=labslug,parent__slug=slug)