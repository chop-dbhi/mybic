import datetime
from haystack import indexes
from mybic.labs.models import Project
from mybic.labs.models import ProjectFile
from news.models import Article
from django.template import loader, Context
from haystack.backends.solr_backend import SolrSearchBackend

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    project_name = indexes.CharField(model_attr='name')
    project_description = indexes.CharField(model_attr='description',null=True)
    project_created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    article_title = indexes.CharField(model_attr='title')
    article_body = indexes.CharField(model_attr='body')
    article_summary = indexes.CharField(model_attr='summary')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class FileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    filepath = indexes.CharField(model_attr='filepath')

    def get_model(self):
        return ProjectFile

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare(self, obj):
        data = super(FileIndex, self).prepare(obj)

        # This could also be a regular Python open() call, a StringIO instance
        # or the result of opening a URL. Note that due to a library limitation
        # file_obj must have a .name attribute even if you need to set one
        # manually before calling extract_file_contents:
        #file_obj = obj.filepath.open()
        file_obj = open(obj.filepath, "rb")

        #https://github.com/courseportal/coursePortal/blob/10aad71186452c55c72507e83c7ee0a7e6372fe0/haystack/search_indexes.py
        extracted_data = self._get_backend(None).extract_file_contents(file_obj)

        # Now we'll finally perform the template processing to render the
        # text field with *all* of our metadata visible for templating:
        t = loader.select_template(('search/indexes/labs/projectfile_text.txt', ))
        data['text'] = t.render(Context({'object': obj,
                                        'extracted': extracted_data}))

        return data