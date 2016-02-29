# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2016 OnlineGroups.net and Contributors.
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
from datetime import date
from mock import (MagicMock, patch, PropertyMock)
from unittest import TestCase
from gs.site.stats.posting import (SitePostingStats, )


class TestSitePostingStats(TestCase):
    '''Test the ``SitePostingStats`` class'''

    @patch.object(SitePostingStats, 'query', new_callable=PropertyMock)
    def test_postStats_sorted(self, m_q):
        'Test that the post-stats are sorted'
        m_q().posts_per_day_on_site.return_value = [
            self.post_stat(2, date(2016, 2, 29)), self.post_stat(1, date(2016, 2, 28)),
            self.post_stat(3, date(2016, 3, 1)), ]
        s = SitePostingStats(MagicMock(), MagicMock())
        r = s.postStats

        self.assertEqual(3, len(r))
        self.assertEqual(1, r[0]['n_posts'])
        self.assertEqual(3, r[-1]['n_posts'])

    @patch.object(SitePostingStats, 'postStats', new_callable=PropertyMock)
    def test_no_posts(self, m_pS):
        'Test that the postsExist property returns False if there are no posts'
        m_pS.return_value = []
        s = SitePostingStats(MagicMock(), MagicMock())
        r = s.postsExist

        self.assertFalse(r)

    @patch.object(SitePostingStats, 'postStats', new_callable=PropertyMock)
    def test_posts(self, m_pS):
        'Test that the postsExist property returns True if there are posts'
        m_pS.return_value = ['a', 'post', ]
        s = SitePostingStats(MagicMock(), MagicMock())
        r = s.postsExist

        self.assertTrue(r)

    @patch.object(SitePostingStats, 'postStats', new_callable=PropertyMock)
    def test_min_no_posts(self, m_pS):
        'Test that the minPerDay property returns 0 if there are no posts'
        m_pS.return_value = []
        s = SitePostingStats(MagicMock(), MagicMock())
        r = s.minPerDay

        self.assertEqual(0.0, r)

    @staticmethod
    def post_stat(n=1, date=date.today()):
        retval = {'n_posts': n,
                  'date': date, }
        return retval

    @patch.object(SitePostingStats, 'postStats', new_callable=PropertyMock)
    def test_min_posts(self, m_pS):
        'Test that the minPerDay property'
        m_pS.return_value = [self.post_stat(2), self.post_stat(3), self.post_stat(1), ]
        s = SitePostingStats(MagicMock(), MagicMock())
        r = s.minPerDay

        self.assertEqual(1, r)

    @patch.object(SitePostingStats, 'postStats', new_callable=PropertyMock)
    def test_max_no_posts(self, m_pS):
        'Test that the maxPerDay property if there are no posts'
        m_pS.return_value = []
        s = SitePostingStats(MagicMock(), MagicMock())
        r = s.maxPerDay

        self.assertEqual(0, r)

    @patch.object(SitePostingStats, 'postStats', new_callable=PropertyMock)
    def test_max_posts(self, m_pS):
        'Test that the minPerDay property'
        m_pS.return_value = [self.post_stat(2), self.post_stat(3), self.post_stat(1), ]
        s = SitePostingStats(MagicMock(), MagicMock())
        r = s.maxPerDay

        self.assertEqual(3, r)

    @patch.object(SitePostingStats, 'postStats', new_callable=PropertyMock)
    def test_mean_posts(self, m_pS):
        'Test that the meanPerDay property'
        m_pS.return_value = [
            self.post_stat(1, date(2016, 2, 28)),
            self.post_stat(2, date(2016, 2, 29)),
            self.post_stat(3, date(2016, 3, 1)), ]

        s = SitePostingStats(MagicMock(), MagicMock())
        r = s.meanPerDay

        self.assertEqual(3.0, r)

    @patch.object(SitePostingStats, 'postStats', new_callable=PropertyMock)
    def test_mean_posts_none(self, m_pS):
        'Test that the meanPerDay property if there are no posts'
        m_pS.return_value = []

        s = SitePostingStats(MagicMock(), MagicMock())
        with self.assertRaises(IndexError):  # --=mpj17=-- Do better
            s.meanPerDay

    @patch.object(SitePostingStats, 'postStats', new_callable=PropertyMock)
    def test_mean_posts_one(self, m_pS):
        'Test that the meanPerDay property returns 0 if there is just one day of posting'
        m_pS.return_value = [self.post_stat(2, date(2016, 2, 29)), ]

        s = SitePostingStats(MagicMock(), MagicMock())
        r = s.meanPerDay

        self.assertEqual(0.0, r)
