#-*- encoding:utf8 -*-
from __future__ import unicode_literals, absolute_import

import unittest

from nta.models import (
    Buttons, ButtonText, ButtonPay, ButtonLink, ButtonOption
)


class TestNaverTalkApi(unittest.TestCase):

    def test_text_button(self):
        btn = ButtonText('test_title', 'test_payload')
        self.assertEqual(btn, {'type': 'TEXT', 'data': {'title': 'test_title', 'code': 'test_payload'}})

    def test_link_button(self):
        btn = ButtonLink('test_title', 'test_url.com')
        self.assertEqual(
            btn,
            {'type': 'LINK', 'data': {'title': 'test_title', 'url': 'test_url.com', 'mobileUrl': None}}
        )

    def test_option_button(self):
        btn = ButtonOption('test_title', [ButtonText('under_option_button')])
        self.assertEqual(
            btn,
            {
                'type': 'OPTION',
                'data': {
                    'title': 'test_title',
                    'buttonList': [{'type': 'TEXT',
                                    'data': {
                                        'title': 'under_option_button'
                                    }}]
                }
            }
        )

if __name__ == '__main__':
    unittest.main()