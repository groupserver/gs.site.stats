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
from __future__ import absolute_import
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from zope.contentprovider.interfaces import UpdateNotCalled
from gs.viewlet.contentprovider import SiteContentProvider
from .posting import SitePostingStats


class SiteStatsContentProvider(SiteContentProvider):

    def __init__(self, context, request, view):
        SiteContentProvider.__init__(self, context, request, view)
        self.__updated = False

    def update(self):
        self.__updated = True

        self.sitePostingStats = SitePostingStats(self.siteInfo,
                                                 self.context)
        self.sitePostingStats.update()

    def render(self):
        if not self.__updated:
            raise UpdateNotCalled

        pageTemplate = PageTemplateFile(self.pageTemplateFileName)
        return pageTemplate(view=self)

    #########################################
    # Non standard methods below this point #
    #########################################
