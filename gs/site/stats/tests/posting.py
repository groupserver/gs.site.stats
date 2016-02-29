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
from mock import (MagicMock, patch, PropertyMock)
from unittest import TestCase
from gs.site.stats.posting import (SitePostingStats, )


class TestSitePostingStats(TestCase):
    '''Test the ``SitePostingStats`` class'''

    @patch.object(SitePostingStats, 'postStats', new_callable=PropertyMock)
    def test_no_posts(self, m_pS):
        'Test that the postsExist property returns False if there are no posts'
        m_pS.return_value = []
        s = SitePostingStats(MagicMock(), MagicMock())
        r = s.postsExist

        self.assertFalse(r)
