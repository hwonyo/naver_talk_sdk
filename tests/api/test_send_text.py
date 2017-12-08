#-*- encoding:utf-8 -*-
import json
import unittest
import responses
try:
    from unittest import mock
except:
    import mock


from nta import (
    NaverTalkApi,
)
from nta.models import(
    TextContent, QuickReply, ButtonText, ButtonLink
)


class TestNaverTalkAPI(unittest.TestCase):
    def setUp(self):
        self.tested = NaverTalkApi('test_naver_talk_access_token')

    @responses.activate
    def test_send_text(self):
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
            self.assertEqual(res.result_code, "00")
            self.assertEqual(res.success, True)
            self.assertEqual(
                payload,
                {
                    'event': 'send',
                    'user': 'test_user_id',
                    'textContent': {
                        'text': 'test_str_message',
                        'code': None,
                        'inputType': None
                    },
                    'options': {
                        'notification': False
                    }
                }
            )
            counter()

        self.tested.send(
            'test_user_id',
            'test_str_message',
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 1)

        self.tested.send(
            user_id='test_user_id',
            message=TextContent('test_str_message'),
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 2)



    @responses.activate
    def test_send_with_quick_reply(self):
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
            self.assertEqual(res.result_code, "00")
            self.assertEqual(res.success, True)
            self.assertEqual(
                payload,
                {
                    "event": "send",
                    "user": "test_user_id",
                    "options": {
                        "notification": False
                    },
                    "textContent": {
                        "code": None,
                        "inputType": None,
                        "quickReply": {
                            "buttonList": [{
                                              "data": {
                                                  "code": "PAYLOAD",
                                                  "title": "text"},
                                              "type": "TEXT"},
                                          {
                                              "data": {
                                                  "mobileUrl": None,
                                                  "title": "text",
                                                  "url": "PAYLOAD"},
                                              "type": "LINK"}]},
                                      "text": "test_str_message"}
                }
            )

            counter()

        self.tested.send(
            'test_user_id',
            'test_str_message',
            quick_reply=QuickReply(
                [
                    {'type': 'TEXT', 'title': 'text', 'value': 'PAYLOAD'},
                    {'type': 'LINK', 'title': 'text', 'value': 'PAYLOAD'}
                ]
            ),
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 1)

        self.tested.send(
            'test_user_id',
            'test_str_message',
            quick_reply=[
                ButtonText('text', 'PAYLOAD'),
                ButtonLink('text', 'PAYLOAD')
            ],
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 2)