import logging
import traceback

from django.conf import settings
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.core.mail import get_connection
from django.views.debug import ExceptionReporter, get_exception_reporter_filter

import re
import sys
from mybic.labs.models import Project


class ProjectEmailHandler(logging.Handler):
    """An exception log handler that emails log entries to project admins.
    If the request is passed as the first argument to the log record,
    request data will be provided in the email report.
    """

    def __init__(self, include_html=False, email_backend=None):
        logging.Handler.__init__(self)
        self.include_html = include_html
        self.email_backend = email_backend

    def emit(self, record):
        try:
            print >>sys.stderr, 'projectemailhandler'
            request = record.request
            subject = '%s (%s IP): %s' % (
                record.levelname,
                ('internal' if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS
                 else 'EXTERNAL'),
                record.getMessage()
            )
            filter = get_exception_reporter_filter(request)
            request_repr = filter.get_request_repr(request)
        except Exception:
            subject = '%s: %s' % (
                record.levelname,
                record.getMessage()
            )
            request = None
            request_repr = "Request repr() unavailable."
        subject = self.format_subject(subject)

        if record.exc_info:
            exc_info = record.exc_info
            stack_trace = '\n'.join(traceback.format_exception(*record.exc_info))
        else:
            exc_info = (None, record.getMessage(), None)
            stack_trace = 'No stack trace available'

        project_url_pattern = re.compile(r'^labs/([\w-]+)/([\w-]+)')
        match = re.search(project_url_pattern, request.path)

        if match:
            lab_slug, project_slug = match.group(1, 2)

            project = Project.objects.filter(lab__slug=lab_slug, slug=project_slug)

            message = "As the owner of the %s project you are receiving this error. Perhaps a link is broken.\n%s\n\n%s" % (project.name, stack_trace, request_repr)
            reporter = ExceptionReporter(request, is_email=True, *exc_info)
            html_message = reporter.get_traceback_html() if self.include_html else None

            mail.mail_owner(project, subject, message, fail_silently=True,
                            html_message=html_message,
                            connection=self.connection())

    def connection(self):
        return get_connection(backend=self.email_backend, fail_silently=True)

    def format_subject(self, subject):
        """
        Escape CR and LF characters, and limit length.
        RFC 2822's hard limit is 998 characters per line. So, minus "Subject: "
        the actual subject must be no longer than 989 characters.
        """
        formatted_subject = subject.replace('\n', '\\n').replace('\r', '\\r')
        return formatted_subject[:989]


def mail_owner(project, subject, message, fail_silently=False, connection=None,
               html_message=None):
    """Sends a message to the admins, as defined by the ADMINS setting."""
    if not settings.ADMINS:
        return
    mail = EmailMultiAlternatives('%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject),
                                  message, settings.SERVER_EMAIL, project.owner.email,
                                  connection=connection)
    if html_message:
        mail.attach_alternative(html_message, 'text/html')
    mail.send(fail_silently=fail_silently)