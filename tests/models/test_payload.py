#-*- encoding:utf8 -*-
from __future__ import unicode_literals, absolute_import

import unittest

from nta.models.payload import (
    PersistentMenuPayload
)
from nta import Button

class TestNaverTalkPayload(unittest.TestCase):
    def test_persistent_menu(self):
        target = {
            "event":"persistentMenu",
            "menuContent" : [{
                "menus":
                [{
                    "type":"TEXT",
                    "data":{
                        "title":"챗봇 안내",
                        "code":"CHATBOT_GUIDE"
                    }
                },{
                    "type":"LINK",
                    "data":{
                        "title":"이벤트 페이지",
                        "url":"http://your-pc-url.com/event",
                        "mobileUrl":"http://your-mobile-url.com/event"
                    }
                },{
                    "type":"LINK",
                    "data":{
                        "title":"전화하기",
                        "url":"tel:021234567",
                        "mobileUrl": None
                    }
                },{
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
                }]
            }]
        }
        payload = PersistentMenuPayload(
            menus=[
                Button.ButtonText(title='챗봇 안내', code='CHATBOT_GUIDE'),
                Button.ButtonLink(
                    title='이벤트 페이지',
                    url='http://your-pc-url.com/event',
                    mobile_url='http://your-mobile-url.com/event'
                ),
                Button.ButtonLink(
                    title='전화하기',
                    url='tel:021234567'
                ),
                Button.ButtonNested(
                    title='공지사항',
                    menus=[
                        Button.ButtonLink(
                            title="교환/환불 안내",
                            url="http://your-pc-url.com/guide",
                            mobile_url="http://your-mobile-url.com/guide"
                        )
                    ]
                )
            ]
        )
        self.assertEqual(target, payload)

    def test_persistent_menu_with_None(self):
        payload = PersistentMenuPayload()
        self.assertEqual(
            payload,
            {
                "event":"persistentMenu",
                "menuContent" : []
            }
        )