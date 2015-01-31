import logging
import traceback

from django.conf import settings
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.core.mail import get_connection
from django.views.debug import ExceptionReporter, get_exception_reporter_filter

import re
import sys
import json
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

    def emit(self, logrecord):
        print >>sys.stderr, 'projectemailhandler {0} length {1}'.format(logrecord.getMessage(),len(logrecord.getMessage()))
        pro_dict = json.loads(logrecord.getMessage())
        project = Project.objects.get(id=pro_dict['project'])
        path = pro_dict['path']
        try:

            # <LogRecord: protected_file, 40, ./mybic/views.py, 114, "(<Project: mybic_sandbox>, u'dfd.jpg')">
            subject = '%s %s' % (
                project.name,
                'user unsuccessfully attempted to access {0}'.format(path)
            )
        except Exception:
            subject = '%s: %s' % (
                project.name,
                'user unsuccessfully attempted to access {0}'.format(path)
            )
            request = None
            request_repr = "Request repr() unavailable."
        subject = self.format_subject(subject)

        message = "As the owner of the {0} project you are receiving this error. This link is broken: {1}".format(project.name, path)

        self.mail_owner(project, subject, message,
                        html_message=None,
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


    def mail_owner(self, project, subject, message, fail_silently=False, connection=None,
                   html_message=None):
        """Sends a message to the admins, as defined by the ADMINS setting."""
        if not settings.ADMINS:
            return
        mail = EmailMultiAlternatives('%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject),
                                      message, settings.SERVER_EMAIL, [project.owner.email],
                                      connection=connection)
        if html_message:
            mail.attach_alternative(html_message, 'text/html')
        mail.send(fail_silently=fail_silently)