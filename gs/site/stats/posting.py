# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from zope.cachedescriptors.property import Lazy
from gs.group.member.base import get_group_userids
from gs.group.stats import MessageQuery


class SitePostingStats(object):
    def __init__(self, siteInfo, context):
        self.siteInfo = siteInfo
        self.context = context

    def update(self):
        # Update the postStats
        foo = self.postStats  # lint:ok
        return None

    @Lazy
    def postStats(self):
        retval = self.query.posts_per_day_on_site(self.siteInfo.id)
        retval.sort(key=lambda x: x['date'])
        return retval

    @Lazy
    def query(self):
        retval = MessageQuery(self.context)
        return retval

    @Lazy
    def postsExist(self):
        retval = False
        if self.postStats:
            retval = len(self.postStats) > 0
        assert type(retval) == bool
        return retval

    @Lazy
    def minPerDay(self):
        retval = 0
        if self.postStats:
            retval = min([s['n_posts'] for s in self.postStats])
        return retval

    @Lazy
    def maxPerDay(self):
        retval = 0
        if self.postStats:
            retval = max([s['n_posts'] for s in self.postStats])
        return retval

    @Lazy
    def meanPerDay(self):
        deltaT = self.postStats[-1]['date'] - self.postStats[0]['date']
        if deltaT.days > 0:
            nPosts = float(sum([s['n_posts'] for s in self.postStats]))
            mean = nPosts / deltaT.days
        else:
            mean = 0.0
        assert type(mean) == float
        return mean

    @Lazy
    def intMeanPerDay(self):
        return int(self.meanPerDay + 0.5)

    @Lazy
    def numMembers(self):
        ids = get_group_userids(self.context, self.siteInfo)
        retval = len(ids)
        return retval
