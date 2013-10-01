# -*- coding: utf-8 -*-
from __future__ import absolute_import
import datetime as dt
from .view import GSSiteStatsView


class GSSiteStatsCSVView(GSSiteStatsView):
    def __call__(self):
        retval = 'ID, Group, Year, Count, Jan, Feb, Mar, Apr, May, Jun, Jul,'\
            ' Aug, Sep, Oct, Nov, Dec\n'
        stats = self.get_stats()
        today = dt.date.today()
        for groupStats in stats:
            group = groupStats['group']
            groupName = group.get_name()
            groupId = group.id
            siteId = self.siteInfo.id

            # Add a row for total group membership
            retval += '"%s", "%s", %s, Total Members,' % \
                (groupId, groupName, today.year)
            members_values = [' '] * 12
            groupMembersInfo = self.get_group_members_info(group.groupObj)
            fullMembers = groupMembersInfo.fullMemberCount
            members_values[today.month - 1] = '%s' % fullMembers
            retval += ','.join(members_values)
            retval += '\n'

            # Add a row for each type of membership
            mad = self.get_members_at_date(group.groupObj)
            membersOnDigest = mad.members_on_digest(siteId, groupId)
            membersOnWebOnly = mad.members_on_webonly(siteId, groupId)
            membersOnEmail = fullMembers - (membersOnDigest + membersOnWebOnly)

            retval += '"%s", "%s", %s, Email Members,' % \
                (groupId, groupName, today.year)
            members_values[today.month - 1] = '%s' % membersOnEmail
            retval += ','.join(members_values)
            retval += '\n'

            retval += '"%s", "%s", %s, Digest Members,' % \
                (groupId, groupName, today.year)
            members_values[today.month - 1] = '%s' % membersOnDigest
            retval += ','.join(members_values)
            retval += '\n'

            retval += '"%s", "%s", %s, Web Only Members,' % \
                (groupId, groupName, today.year)
            members_values[today.month - 1] = '%s' % membersOnWebOnly
            retval += ','.join(members_values)
            retval += '\n'

            years = groupStats['stats'].keys()
            years.reverse()
            for year in years:
                retval += '"%s", "%s", %s, Posts' % (groupId, groupName, year)
                for m in range(1, 13):
                    monthStats = groupStats['stats'][year].get(m, {})
                    retval += ', %s' % monthStats.get('post_count', 0)
                retval += '\n"%s", "%s", %s, Authors' % \
                    (groupId, groupName, year)
                for m in range(1, 13):
                    monthStats = groupStats['stats'][year].get(m, {})
                    retval += ', %s' % monthStats.get('user_count', 0)
                retval += '\n'
        assert retval
        return retval
