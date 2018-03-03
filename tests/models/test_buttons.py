#-*- encoding:utf8 -*-
from __future__ import unicode_literals, absolute_import

import unittest

from nta.models import (
    Buttons, ButtonText, ButtonPay, ButtonLink, ButtonOption, ButtonNested, ButtonTime,
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
        btn1 = ButtonLink('test_title', 'test_url.com')
        self.assertEqual(
            btn1,
            {'type': 'LINK', 'data': {'title': 'test_title', 'url': 'test_url.com', 'mobileUrl': None}}
        )

        btn2 = ButtonLink(
            'test_webview_button',
            'test_url.com',
            'test_webview_url.com',
            webview=True,
            webview_title='webview_title',
            webview_height=50
        )
        self.assertEqual(
            btn2,
            {'type': 'LINK',
             'data': {
                 'title': 'test_webview_button',
                 'url': 'test_url.com',
                 'mobileUrl': 'test_webview_url.com',
                 'mobileTarget': 'webview',
                 'mobileTargetAttr': {
                     'webviewHeight': 50,
                     'webviewTitle': 'webview_title'
                 }}
             }
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

    def test_pay_button(self):
        product_item = ProductItem(
            category_type='FOOD',
            category_id='DELIVERY',
            uid='bot-product-1234',
            name='yo',
            start_date='20171130',
            end_date='20171201',
            seller_id='hollal',
            count=1
        )
        payinfo = PaymentInfo(
            merchant_pay_key='bot-pay=1234',
            total_pay_amount=15000,
            product_items=[product_item],
            merchant_user_key=1,
            product_name='test_product',
            product_count=1,
            delivery_fee=1,
            tax_scope_amount=1,
            tax_ex_scope_amount=1,
            purchaser_name='hwang',
            purchaser_birthday='0726'
        )
        btn = ButtonPay(payinfo)
        self.assertEqual(
            btn,
            {
                'type': 'PAY',
                'data': {
                    'paymentInfo': {
                        'merchantPayKey': 'bot-pay=1234',
                        'totalPayAmount': 15000,
                        'productItems': [
                            {
                                'categoryType': 'FOOD',
                                'categoryId': 'DELIVERY',
                                'uid': 'bot-product-1234',
                                'name': 'yo',
                                'startDate': '20171130',
                                'endDate': '20171201',
                                'sellerId': 'hollal',
                                'count': 1
                            }
                        ],
                        'merchantUserKey': 1,
                        'productName': 'test_product',
                        'productCount': 1,
                        'deliveryFee': 1,
                        'taxScopeAmount': 1,
                        'taxExScopeAmount': 1,
                        'purchaserName': 'hwang',
                        'purchaserBirthday': '0726'
                    }
                }
            }
        )

    def test_button_nested(self):
        target = {
			"type":"NESTED",
			"data":{
				"title":"공지사항",
				"menus":
				[{
					"type":"LINK",
					"data":{
						"title":"교환/환불 안내",
						"url":"http://your-pc-url.com/guide",
						"mobileUrl":"http://your-mobile-url.com/guide"
					}
				}]
			}
        }
        btn = ButtonNested(
            title='공지사항',
            menus=[
                ButtonLink(
                    title='교환/환불 안내',
                    url='http://your-pc-url.com/guide',
                    mobile_url='http://your-mobile-url.com/guide'
                )
            ]
        )

        self.assertEqual(btn, target)

    def test_time_button(self):
        target = {
            "type": "TIME",
            "data": {
                "title": "타이틀",
                "code": "코드"
            }
        }
        btn = ButtonTime(
            title='타이틀',
            code='코드'
        )
        self.assertEqual(target, btn)




if __name__ == '__main__':
    unittest.main()