""" scrape project pages
"""
from optparse import make_option
import re
import sys
import traceback
from mybic.labs.models import Project,Lab
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import scrapy

