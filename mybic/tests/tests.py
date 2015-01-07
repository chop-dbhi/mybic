from django.core import mail
from django.test import TestCase
from django.contrib.auth.models import User,Group
from mybic.labs.models import Project,Lab

class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail('Regarding your Django tests', 'You have inherited millions!',
            'from@mybic.chop.edu', ['leipzigj@email.chop.edu'],
            fail_silently=False)
        self.assertEquals(len(mail.outbox), 1)



class LabTestCase(TestCase):
    def setUp(self):
        frankengroup=Group.objects.create(name="FrankenGroup")
        frankenstein=User.objects.create(username="frankie10101",first_name="Dr.",last_name="Frankenstein")
        frankenlab=Lab.objects.create(name="Dr. Frankenstein's Crazy Lab", pi=frankenstein, group=frankengroup, slug="FrankenLab")
    def test_obs(self):
        frankenlab=Lab.objects.get(slug="FrankenLab")
        self.assertEquals(frankenlab.pi.last_name,"Frankenstein")