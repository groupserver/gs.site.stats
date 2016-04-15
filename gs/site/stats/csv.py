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
        '''Write a value in at a particular month

:param val: The value to show.
:param int month: The month the value is shown at (1 to 12 inclusive)
:returns: Twelve CSV cells with the value in the nth cell (counting from 1)
:rtype: unicode'''
        months = [' ', ] * 12
        i = month - 1
        months[i] = '{0}'.format(val)
        retval = ','.join(months)
        return retval

    @staticmethod
    def item_row(groupInfo, year, name, value):
        '''A standard CSV row

:param groupInfo: The group to display the row for.
:param int year: The year to display the row for.
:param str name: The name of the row.
:param value: The value to display.
:returns: A five-cell CSV row: "groupId, groupName, year, name, value\\n"
:rtype: unicode'''
        r = '"{groupInfo.id}", "{groupInfo.name}", {year}, "{name}", {value}\n'
        retval = r.format(groupInfo=groupInfo, year=year, name=name, value=value)
        return retval

    def item_row_at_month(self, groupInfo, name, value):
        '''Write a value for a group for the current month and year

:param groupInfo: The group to display the row for.
:param str name: The name of the row.
:param value: The value to display.
:returns: A line representing sixteen CSV cells. The value will be in the "4+month" cell
          (counting from 1).
:rtype: unicode'''
        v = self.value_at_month(value, self.today.month)
        retval = self.item_row(groupInfo, self.today.year, name, v)
        return retval

    def set_response_header(self):
        response = self.request.response
        response.setHeader(b"Content-Type", b'text/csv; charset=UTF-8')
        filename = '{0}-statistics.csv'.format(self.siteInfo.id)
        disposition = 'inline; filename="{0}"'.format(filename)
        response.setHeader(b'Content-Disposition', to_ascii(disposition))

    def group_member_stats(self, group):
        fullMembers = len(self.get_members(group.groupObj))
        retval = self.item_row_at_month(group, 'Total members', fullMembers)
        mad = self.get_members_at_date(group.groupObj)
        membersOnDigest = mad.members_on_digest(self.siteInfo.id, group.id)
        membersOnWebOnly = mad.members_on_webonly(self.siteInfo.id, group.id)
        membersOnEmail = fullMembers - (membersOnDigest + membersOnWebOnly)
        retval += self.item_row_at_month(group, 'Email members', membersOnEmail)
        retval += self.item_row_at_month(group, 'Digest members', membersOnDigest)
        retval += self.item_row_at_month(group, 'Web-only members', membersOnWebOnly)
        return retval

    def group_monthly_posting_stats(self, group, stats):
        retval = ''
        years = list(stats.keys())
        years.reverse()
        for year in years:
            # Use the fixed list of 12 months, rather than the items in the year so
            # we get 0 values for missing months (``__missing__`` is defined).
            postCounts = ['{0}'.format(stats[year][m]['post_count']) for m in self.MONTHS]
            retval += self.item_row(group, year, 'Posts', ', '.join(postCounts))
            userCounts = ['{0}'.format(stats[year][m]['user_count']) for m in self.MONTHS]
            retval += self.item_row(group, year, 'Authors', ', '.join(userCounts))
        return retval

    def __call__(self):
        self.set_response_header()
        r = self.HEAD
        for groupStats in self.get_stats():
            group = groupStats['group']
            r += self.group_member_stats(group)
            stats = groupStats['stats']
            r += self.group_monthly_posting_stats(group, stats)
        retval = r.encode('utf-8', 'ignore')
        assert retval
        return retval
