# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2016 OnlineGroups.net and Contributors.
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
from zope.cachedescriptors.property import Lazy
from gs.core import to_ascii
from .view import GSSiteStatsView


class GSSiteStatsCSVView(GSSiteStatsView):

    #: The first row of the spreadsheet
    HEAD = 'ID, Group, Year, Count, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec\n'

    #: The list of months is used rather a lot
    MONTHS = list(range(1, 13))

    @Lazy
    def today(self):
        'The date for today. Used a lot, and because midnight.'
        retval = date.today()
        return retval

    @staticmethod
    def value_at_month(val, month):
        months = [' ', ] * 12
        i = month - 1
        months[i] = '{0}'.format(val)
        retval = ','.join(months)
        return retval

    @staticmethod
    def item_row(groupInfo, year, name, value):
        r = '"{groupInfo.id}", "{groupInfo.name}", {year}, "{name}", {value}\n'
        retval = r.format(groupInfo=groupInfo, year=year, name=name, value=value)
        return retval

    def item_row_at_month(self, groupInfo, name, value):
        v = self.value_at_month(value, self.today.month)
        retval = self.item_row(groupInfo, self.today.year, name, v)
        return retval

    def set_response_header(self):
        response = self.request.response
        response.setHeader(b"Content-Type", b'text/csv; charset=UTF-8')
        filename = '{0}-statistics.csv'.format(self.siteInfo.id)
        disposition = 'inline; filename="{0}"'.format(filename)
        response.setHeader(b'Content-Disposition', to_ascii(disposition))

    def __call__(self):
        self.set_response_header()
        r = self.HEAD

        for groupStats in self.get_stats():
            group = groupStats['group']

            fullMembers = len(self.get_members(group.groupObj))
            r += self.item_row_at_month(group, 'Total members', fullMembers)

            # Add a row for each type of membership
            mad = self.get_members_at_date(group.groupObj)
            membersOnDigest = mad.members_on_digest(self.siteInfo.id, group.id)
            membersOnWebOnly = mad.members_on_webonly(self.siteInfo.id, group.id)
            membersOnEmail = fullMembers - (membersOnDigest + membersOnWebOnly)
            r += self.item_row_at_month(group, 'Email members', membersOnEmail)
            r += self.item_row_at_month(group, 'Digest members', membersOnDigest)
            r += self.item_row_at_month(group, 'Web-only members', membersOnWebOnly)

            stats = groupStats['stats']
            years = list(stats.keys())
            years.reverse()
            for year in years:
                # Use the fixed list of 12 months, rather than the items in the year so
                # we get 0 values for missing months (``__missing__`` is defined).
                postCounts = ['{0}'.format(stats[year][m]['post_count']) for m in self.MONTHS]
                r += self.item_row(group, year, 'Posts', ', '.join(postCounts))
                userCounts = ['{0}'.format(stats[year][m]['user_count']) for m in self.MONTHS]
                r += self.item_row(group, year, 'Authors', ', '.join(userCounts))
        retval = r.encode('utf-8', 'ignore')
        assert retval
        return retval
