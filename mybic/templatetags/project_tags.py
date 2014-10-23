from django import template
from django.core import urlresolvers
from django.conf import settings
import datetime
import urlparse
import os 
register = template.Library()

def slink(context, url_name):
    """ Render a path to a project static symlink """
    return os.path.join(context['static_link'],url_name)

register.simple_tag(takes_context=True)(slink)

def do_current_time(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return CurrentTimeNode(format_string[1:-1])

class CurrentTimeNode(template.Node):
    def __init__(self, format_string):
        self.format_string = format_string
    def render(self, context):
        return datetime.datetime.now().strftime(self.format_string)
        
register.tag('current_time', do_current_time)