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
    def test_thread_taking(self):
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
                    'event': 'handover',
                    'user': 'test_user_id',
                    'options': {
                        "control": "takeThread",
                        "metadata": ""
                    }
                }
            )
            counter()

        self.tested.take_thread(
            user_id='test_user_id',
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 1)

    @responses.activate
    def test_thread_passing(self):
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
                    'event': 'handover',
                    'user': 'test_user_id',
                    'options': {
                        "control": "passThread",
                        "targetId": 1
                    }
                }
            )
            counter()

        self.tested.pass_thread(
            user_id='test_user_id',
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 1)