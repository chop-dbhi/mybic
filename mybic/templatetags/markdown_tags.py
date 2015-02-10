from django import template
from django.utils.safestring import mark_safe
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

import mistune



register = template.Library()


@register.filter(name="markdown")
def markdown_filter(value):
    """Processes the given value as Markdown using mistune

    Syntax::

        {{ value|markdown }}            {# uses the "default" style #}

    """
    try:
        return mark_safe(mistune.markdown(value))
    except ImportError:
        raise template.TemplateSyntaxError("Error in `markdown` tag: "
                    "The mistune library isn't installed.")
markdown_filter.is_safe = True


@register.tag(name="markdown")
def markdown_tag(parser, token):
    nodelist = parser.parse(('endmarkdown',))

    parser.delete_first_token() # consume '{% endmarkdown %}'
    return MarkdownNode(nodelist)

class MarkdownNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        value = self.nodelist.render(context)
        try:
            return mark_safe(mistune.markdown(value))
        except ImportError:
            raise template.TemplateSyntaxError("Error in `markdown` tag: "
                    "The mistune library isn't installed.")
