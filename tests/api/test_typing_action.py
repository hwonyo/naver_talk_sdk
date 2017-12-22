#-*- encoding:utf-8 -*-
import unittest
import responses
try:
    from unittest import mock
except:
    import mock


from nta import (
    NaverTalkApi
)


class TestNaverTalkActionEvent(unittest.TestCase):
    def setUp(self):
        self.tested = NaverTalkApi('test_naver_talk_access_token')

    @responses.activate
    def test_typing_on(self):
        responses.add(
            responses.POST,
            NaverTalkApi.DEFAULT_API_ENDPOINT,
            json={
                "success": True,
                "resultCode": "00",
            },
            status=200
        )

        counter = mock.MagicMock()
        def test_callback(res, payload):
            self.assertEqual(res.result_code, "00")
            self.assertEqual(res.success, True)
            self.assertEqual(payload.user, 'test_user_id')
            self.assertEqual(payload.event, 'action')
            self.assertEqual(payload.options, {"action": "typingOn"})
            counter()

        self.tested.typing_on('test_user_id', callback=test_callback)
        self.assertEqual(counter.call_count, 1)

    @responses.activate
    def test_typing_off(self):
        responses.add(
            responses.POST,
            NaverTalkApi.DEFAULT_API_ENDPOINT,
            json={
                "success": True,
                "resultCode": "00",
            },
            status=200
        )

        counter = mock.MagicMock()
        def test_callback(res, payload):
            self.assertEqual(res.result_code, "00")
            self.assertEqual(res.success, True)
            self.assertEqual(payload.user, 'test_user_id')
            self.assertEqual(payload.event, 'action')
            self.assertEqual(payload.options, {"action": "typingOff"})
            counter()

        self.tested.typing_off('test_user_id', callback=test_callback)
        self.assertEqual(counter.call_count, 1)