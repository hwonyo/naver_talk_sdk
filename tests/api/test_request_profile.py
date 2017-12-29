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


class TestNaverTalkAPI(unittest.TestCase):
    def setUp(self):
        self.tested = NaverTalkApi('test_naver_talk_access_token')

    @responses.activate
    def test_request_profile(self):
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
                payload.options,
                {
                    "field": "nickname",
                    "agreements": ["cellphone", "address"]
                }
            )
            counter()

        self.tested.request_profile(
            'test_id',
            'nickname',
            agreements=['cellphone', 'address'],
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 1)