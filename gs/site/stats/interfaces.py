# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from zope.schema import ASCIILine
from zope.contentprovider.interfaces import IContentProvider
from gs.core import to_ascii
from . import GSMessageFactory as _


class IGSSiteStatsContentProvider(IContentProvider):
    siteId = ASCIILine(
        title=_('Site Identifier'),
        description=_('The identifier for the site'),
        required=True)

    pageTemplateFileName = ASCIILine(
        title=_("Page Template File Name"),
        description=_('The name of the ZPT file that is used to '
                      'render the status message.'),
        required=False,
        default=to_ascii("browser/templates/contentprovider.pt"))
