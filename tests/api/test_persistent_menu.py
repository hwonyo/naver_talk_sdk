#-*- encoding:utf-8 -*-
import json
import unittest
import responses
try:
    from unittest import mock
except:
    import mock


from nta import (
    NaverTalkApi, Button
)
from nta.models import(
    TextContent, QuickReply, ButtonText, ButtonLink
)


class TestNaverTalkAPI(unittest.TestCase):
    def setUp(self):
        self.tested = NaverTalkApi('test_naver_talk_access_token')

    @responses.activate
    def test_persistent_menu(self):
        responses.add(
            responses.POST,
            NaverTalkApi.DEFAULT_API_ENDPOINT,
            json={
                "success": True,
                "resultCode": "00"
            },
            status=200
        )

        counter = mock.MagicMock()
        def test_callback(res, payload):
            self.assertEqual(
                payload,
                {
                    "event": "persistentMenu",
                    "menuContent": [{
                        "menus":
                            [{
                                "type": "TEXT",
                                "data": {
                                    "title": "챗봇 안내",
                                    "code": "CHATBOT_GUIDE"
                                }
                            }, {
                                "type": "LINK",
                                "data": {
                                    "title": "이벤트 페이지",
                                    "url": "http://your-pc-url.com/event",
                                    "mobileUrl": "http://your-mobile-url.com/event"
                                }
                            }, {
                                "type": "LINK",
                                "data": {
                                    "title": "전화하기",
                                    "url": "tel:021234567",
                                    "mobileUrl": None
                                }
                            }, {
                                "type": "NESTED",
                                "data": {
                                    "title": "공지사항",
                                    "menus":
                                        [{
                                            "type": "LINK",
                                            "data": {
                                                "title": "교환/환불 안내",
                                                "url": "http://your-pc-url.com/guide",
                                                "mobileUrl": "http://your-mobile-url.com/guide"
                                            }
                                        }]
                                }
                            }]
                    }]
                }
            )
            counter()

        self.tested.persistent_menu(
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
            ],
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 1)

    @responses.activate
    def test_persistent_menu_with_None(self):
        responses.add(
            responses.POST,
            NaverTalkApi.DEFAULT_API_ENDPOINT,
            json={
                "success": True,
                "resultCode": "00"
            },
            status=200
        )

        counter = mock.MagicMock()
        def test_callback(res, payload):
            self.assertEqual(
                payload,
                {
                    "event": "persistentMenu",
                    "menuContent": []
                }
            )
            counter()

        self.tested.persistent_menu(callback=test_callback)
        self.assertEqual(counter.call_count, 1)