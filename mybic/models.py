from django.contrib.auth.models import User

class UserMethods(User):
  def get_group_objects(self):
    if user.is_staff:
        return Group.objects.all()
    else:
        my_groups = Group.objects.filter(user=self)
  def get_groups_list(self):
      if user.is_staff:
          return Group.objects.all().values_list('name',flat=True)
      else:
          return Group.objects.filter(user=self).values_list('name', flat=True)
  class Meta:
    proxy=True