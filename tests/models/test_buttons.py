#-*- encoding:utf8 -*-
from __future__ import unicode_literals, absolute_import

import unittest

from nta.models import (
    Buttons, ButtonText, ButtonPay, ButtonLink, ButtonOption,
    PaymentInfo, ProductItem
)


class TestNaverTalkApi(unittest.TestCase):

    def test_button_convert_test(self):
        btns = Buttons.convert_shortcut_buttons(
            [
                {'type': 'TEXT', 'title': 'test_title', 'value': 'test_payload'},
                {'type': 'LINK', 'title': 'test_title', 'value': 'test_url.com'},
                {'type': 'OPTION', 'title': 'test_title', 'value': [{'type': 'TEXT', 'title': 'under_option_button'}]},
                {'type': 'PAY', 'value': PaymentInfo(1,1,1)}
            ]
        )

        self.assertTrue(isinstance(btns[0], ButtonText))
        self.assertTrue(isinstance(btns[1], ButtonLink))
        self.assertTrue(isinstance(btns[2], ButtonOption))
        self.assertTrue(isinstance(btns[3], ButtonPay))
        self.assertEqual(btns[0], ButtonText('test_title', 'test_payload'))
        self.assertEqual(btns[1], ButtonLink('test_title', 'test_url.com'))
        self.assertEqual(btns[2], ButtonOption('test_title', ButtonText('under_option_button')))
        self.assertEqual(btns[3], ButtonPay(PaymentInfo(1,1,1)))


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
        btn = ButtonOption('test_title', ButtonText('under_option_button'))
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

    def test_pay_butotn(self):
        pass

if __name__ == '__main__':
    unittest.main()