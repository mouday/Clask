# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, unicode_literals

from string import Template


class UrlTemplate(Template):
    delimiter = ""
    idpattern = ""
    braceidpattern = r"\w+"
