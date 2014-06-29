from django.contrib.auth.models import User,Group
import mybic.labs.models as models
from django.contrib import admin

#class LabAdmin(admin.ModelAdmin):
#    list_display = ('pi','group')
    #extra = 1

admin.site.unregister(Group)
#admin.site.register(User)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name','directory','lab')

admin.site.register(models.Project,ProjectAdmin)

#admin.site.register(models.Project,LabAdmin)


class LabInline(admin.TabularInline):
    model = models.Lab
    #extra = 1
    #list_display = ('first_name','last_name')


class LabAdmin(admin.ModelAdmin):
    inlines = [LabInline]

admin.site.register(Group,LabAdmin)