# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2016 Michael JasonSmith and Contributors.
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
from __future__ import absolute_import, unicode_literals, print_function
from mock import (MagicMock, patch, PropertyMock, call, )
from unittest import TestCase
from gs.group.stats.messagequery import YearDict
from gs.site.stats.csv import (GSSiteStatsCSVView, )


class TestGSSiteStatsCSVView(TestCase):
    '''Test the ``GSSiteStatsCSVView`` class'''

    @property
    def group(self):
        groupInfo = MagicMock(spec=['id', 'name', 'groupObj', ])
        groupInfo.id = 'ethel'
        groupInfo.name = 'Ethel the frog'
        return groupInfo

    def test_value_at_month(self):
        r = GSSiteStatsCSVView.value_at_month(12, 2)

        expected = ' ,12, , , , , , , , , , '
        self.assertEqual(expected, r)

    def test_item_row(self):
        r = GSSiteStatsCSVView.item_row(self.group, 2016, 'Violence', '"British gangland"')

        expected = '"ethel", "Ethel the frog", 2016, "Violence", "British gangland"\n'
        self.assertEqual(expected, r)

    @patch.object(GSSiteStatsCSVView, 'today', new_callable=PropertyMock)
    def test_item_row_at_month(self, m_today):
        m_today().month = 4
        m_today().year = 2016
        s = GSSiteStatsCSVView(MagicMock(), MagicMock())
        r = s.item_row_at_month(self.group, 'Violence', '"British gangland"')

        expected = ('"ethel", "Ethel the frog", 2016, "Violence",  , , ,"British gangland", , , , '
                    ', , , , \n')
        self.assertEqual(expected, r)

    @patch.object(GSSiteStatsCSVView, 'siteInfo', new_callable=PropertyMock)
    def test_set_response_header(self, m_siteInfo):
        m_siteInfo().id = 'example'
        request = MagicMock()
        s = GSSiteStatsCSVView(MagicMock(), request)
        s.set_response_header()

        calls = [call(b'Content-Type', b'text/csv; charset=UTF-8'),
                 call(b'Content-Disposition', 'inline; filename="example-statistics.csv"'), ]
        request.response.setHeader.assert_has_calls(calls)

    @patch.object(GSSiteStatsCSVView, 'siteInfo', new_callable=PropertyMock)
    @patch.object(GSSiteStatsCSVView, 'get_members')
    @patch.object(GSSiteStatsCSVView, 'get_members_at_date')
    @patch.object(GSSiteStatsCSVView, 'today', new_callable=PropertyMock)
    def test_group_member_stats(self, m_today, m_get_members_at_date, m_get_members, m_siteInfo):
        m_today().month = 4
        m_today().year = 2016
        m_get_members_at_date().members_on_digest.return_value = 1
        m_get_members_at_date().members_on_webonly.return_value = 2
        m_get_members.return_value = [0, 1, 2, 3, 4, 5]
        m_siteInfo().id = 'example'
        s = GSSiteStatsCSVView(MagicMock(), MagicMock())
        r = s.group_member_stats(self.group)

        self.assertIn('"Total members",  , , ,6', r)
        self.assertIn('"Email members",  , , ,3', r)
        self.assertIn('"Web-only members",  , , ,2', r)
        self.assertIn('"Digest members",  , , ,1', r)
        self.assertEqual(4, r.count('\n'))

    def test_group_monthly_posting_stats(self):
        y2016 = YearDict()
        y2016[1] = {'post_count': 9, 'user_count': 3}
        y2016[2] = {'post_count': 25, 'user_count': 4}
        y2016[3] = {'post_count': 29, 'user_count': 6}
        y2016[4] = {'post_count': 22, 'user_count': 8}
        stats = {2016: y2016}

        s = GSSiteStatsCSVView(MagicMock(), MagicMock())
        r = s.group_monthly_posting_stats(self.group, stats)

        self.assertIn('"Posts", 9, 25, 29, 22, 0, 0, 0, 0, 0, 0, 0, 0\n', r)
        self.assertIn('"Authors", 3, 4, 6, 8, 0, 0, 0, 0, 0, 0, 0, 0\n', r)
        self.assertEqual(2, r.count('"ethel", "Ethel the frog", 2016, '))
