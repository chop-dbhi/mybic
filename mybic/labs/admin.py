from django.contrib.auth.models import User, Group
import mybic.labs.models as models
from mybic.labs.models import Project, Lab
from django.contrib import admin
from django.forms import ModelForm
from django import forms
import os
import re
import urllib2

admin.site.unregister(Group)


class ProjectAdminForm(ModelForm):
    def clean(self):
        data = self.cleaned_data
        # data['index_page']
        index_page = data['index_page']
        static_dir = data['static_dir']
        url_pattern = re.compile(r"^https?://.+")

        if url_pattern.match(index_page):
            try:
                urllib2.urlopen(index_page)
            except urllib2.HTTPError, e:
                raise forms.ValidationError("The index page url {0} does not exist".format(index_page))
        else:
            if not os.path.exists(index_page):
                raise forms.ValidationError("The index page file {0} does not exist".format(index_page))
        if not os.path.exists(static_dir):
            raise forms.ValidationError("The static directory {0} does not exist".format(static_dir))
        # do something that validates your data
        return data


# TODO: validate no names like "index.md" are used
# http://stackoverflow.com/questions/877723/inline-form-validation-in-django
class ChildrenInline(admin.TabularInline):
    model = models.ChildIndex


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    inlines = [ChildrenInline]


admin.site.register(models.Project, ProjectAdmin)


class LabInline(admin.TabularInline):
    model = models.Lab


class LabAdmin(admin.ModelAdmin):
    inlines = [LabInline]


admin.site.register(Group, LabAdmin)

admin.site.register(models.Lab)

admin.site.register(models.LabArticle)

admin.site.register(models.ProjectArticle)