# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import absolute_import, unicode_literals
from datetime import date
from gs.core import to_ascii
from .view import GSSiteStatsView


class GSSiteStatsCSVView(GSSiteStatsView):
    def __call__(self):
        r = 'ID, Group, Year, Count, Jan, Feb, Mar, Apr, May, Jun, Jul,'\
            ' Aug, Sep, Oct, Nov, Dec\n'
        stats = self.get_stats()
        today = date.today()
        for groupStats in stats:
            group = groupStats['group']
            groupName = group.get_name()
            groupId = group.id
            siteId = self.siteInfo.id

            # Add a row for total group membership
            r += '"%s", "%s", %s, Total Members,' % \
                (groupId, groupName, today.year)
            members_values = [' '] * 12
            groupMembersInfo = self.get_group_members_info(group.groupObj)
            fullMembers = groupMembersInfo.fullMemberCount
            members_values[today.month - 1] = '%s' % fullMembers
            r += ','.join(members_values)
            r += '\n'

            # Add a row for each type of membership
            mad = self.get_members_at_date(group.groupObj)
            membersOnDigest = mad.members_on_digest(siteId, groupId)
            membersOnWebOnly = mad.members_on_webonly(siteId, groupId)
            membersOnEmail = (fullMembers
                              - (membersOnDigest + membersOnWebOnly))

            r += '"%s", "%s", %s, Email Members,' % \
                (groupId, groupName, today.year)
            members_values[today.month - 1] = '%s' % membersOnEmail
            r += ','.join(members_values)
            r += '\n'

            r += '"%s", "%s", %s, Digest Members,' % \
                (groupId, groupName, today.year)
            members_values[today.month - 1] = '%s' % membersOnDigest
            r += ','.join(members_values)
            r += '\n'

            r += '"%s", "%s", %s, Web Only Members,' % \
                (groupId, groupName, today.year)
            members_values[today.month - 1] = '%s' % membersOnWebOnly
            r += ','.join(members_values)
            r += '\n'

            years = list(groupStats['stats'].keys())
            years.reverse()
            for year in years:
                r += '"%s", "%s", %s, Posts' % (groupId, groupName, year)
                for m in range(1, 13):
                    monthStats = groupStats['stats'][year].get(m, {})
                    r += ', %s' % monthStats.get('post_count', 0)
                r += '\n"%s", "%s", %s, Authors' % \
                    (groupId, groupName, year)
                for m in range(1, 13):
                    monthStats = groupStats['stats'][year].get(m, {})
                    r += ', %s' % monthStats.get('user_count', 0)
                r += '\n'

        response = self.request.response
        ctype = 'text/csv; charset=UTF-8'
        response.setHeader(to_ascii("Content-Type"), to_ascii(ctype))
        filename = '{0}-statistics.csv'.format(self.siteInfo.id)
        disposition = 'inline; filename="{0}"'.format(filename)
        response.setHeader(to_ascii('Content-Disposition'),
                           to_ascii(disposition))
        assert r
        retval = r.encode('utf-8', 'ignore')
        assert retval
        return retval
