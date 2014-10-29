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
from __future__ import unicode_literals
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.content.base.page import SitePage
from gs.group.stats import MembersAtDate, MessageQuery
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo


class GSSiteStatsView(SitePage):
    def __init__(self, context, request):
        super(GSSiteStatsView, self).__init__(context, request)

    @Lazy
    def groupsInfo(self):
        retval = createObject('groupserver.GroupsInfo', self.context)
        return retval

    @Lazy
    def messageQuery(self):
        retval = MessageQuery(self.context)
        return retval

    def get_stats(self):
        siteId = self.siteInfo.get_id()
        groupIds = self.groupsInfo.get_visible_group_ids()
        groupIds.sort()
        retval = {}
        for groupId in groupIds:
            gObj = createObject('groupserver.GroupInfo', self.context,
                                groupId)
            res = self.messageQuery.posting_stats(siteId, [groupId])
            retval = {'group': gObj, 'stats': res}
            yield retval

    def get_group_members_info(self, group):
        """
            Convienence method for templates. Returns an instance of
            IGSGroupMembersInfo for the provided group.
        """
        groupMembersInfo = GSGroupMembersInfo(group)
        assert groupMembersInfo
        return groupMembersInfo

    def get_members_at_date(self, group):
        """
            Convienence method for templates. Returns an instance of
            gs.group.stats.queries.MembersAtDate.
        """
        mad = MembersAtDate(group)
        assert mad
        return mad
