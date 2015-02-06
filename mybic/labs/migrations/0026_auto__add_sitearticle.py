# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'SiteArticle'
        db.create_table(u'labs_sitearticle', (
            (u'article_ptr',
             self.gf('django.db.models.fields.related.OneToOneField')(to=orm['news.Article'], unique=True,
                                                                      primary_key=True)),
        ))
        db.send_create_signal(u'labs', ['SiteArticle'])


    def backwards(self, orm):
        # Deleting model 'SiteArticle'
        db.delete_table(u'labs_sitearticle')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [],
                            {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')",
                     'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True',
                        'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [],
                                 {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True',
                                  'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'labs.childindex': {
            'Meta': {'object_name': 'ChildIndex'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.CharField', [],
                     {'default': "'/mnt/variome/'", 'max_length': '300', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labs.Project']"})
        },
        u'labs.lab': {
            'Meta': {'object_name': 'Lab'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [],
                         {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': (
            'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'pi': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'labs.labarticle': {
            'Meta': {'ordering': "['-created']", 'object_name': 'LabArticle', '_ormbases': [u'news.Article']},
            u'article_ptr': ('django.db.models.fields.related.OneToOneField', [],
                             {'to': u"orm['news.Article']", 'unique': 'True', 'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labs.Lab']"})
        },
        u'labs.project': {
            'Meta': {'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'de_dir': ('django.db.models.fields.CharField', [],
                       {'db_index': 'True', 'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'git_branch': (
            'django.db.models.fields.CharField', [], {'default': "'master'", 'max_length': '100', 'db_index': 'True'}),
            'git_repo': (
            'django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '300', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_page': ('django.db.models.fields.CharField', [],
                           {'default': "'/mnt/variome/'", 'max_length': '300', 'db_index': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labs.Lab']"}),
            'modified': ('django.db.models.fields.DateTimeField', [],
                         {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'static_dir': ('django.db.models.fields.CharField', [],
                           {'default': "'/mnt/variome/'", 'max_length': '300', 'db_index': 'True'})
        },
        u'labs.projectarticle': {
            'Meta': {'ordering': "['-created']", 'object_name': 'ProjectArticle', '_ormbases': [u'news.Article']},
            u'article_ptr': ('django.db.models.fields.related.OneToOneField', [],
                             {'to': u"orm['news.Article']", 'unique': 'True', 'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labs.Project']"})
        },
        u'labs.sitearticle': {
            'Meta': {'ordering': "['-created']", 'object_name': 'SiteArticle', '_ormbases': [u'news.Article']},
            u'article_ptr': ('django.db.models.fields.related.OneToOneField', [],
                             {'to': u"orm['news.Article']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'labs.staff': {
            'Meta': {'object_name': 'staff', '_ormbases': [u'auth.User']},
            'projects': ('django.db.models.fields.related.ManyToManyField', [],
                         {'to': u"orm['labs.Project']", 'symmetrical': 'False'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [],
                          {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'news.article': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Article'},
            'author': ('django.db.models.fields.related.ForeignKey', [],
                       {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ManyToManyField', [],
                         {'blank': 'True', 'related_name': "'articles'", 'null': 'True', 'symmetrical': 'False',
                          'to': u"orm['news.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markup_filter': (
            'django.db.models.fields.PositiveIntegerField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'news.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [],
                       {'to': u"orm['news.Category']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['labs']