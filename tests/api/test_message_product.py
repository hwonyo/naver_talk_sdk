# -*- encoding:utf-8 -*-
import unittest
import responses

try:
    from unittest import mock
except:
    import mock

from nta import (
    NaverTalkApi,
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
                    "event": "product",
                    "options": {
                        "ids": [
                            1002324883,
                            1002793763,
                            2265658394,
                            2299323502
                        ],
                        "displayType": "list"
                    },
                    "user": "test_user_id"
                }
            )
            counter()

        self.tested.product_message(
            'test_user_id',
            ids=[
                1002324883,
                1002793763,
                2265658394,
                2299323502
            ],
            display_type='list',
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 1)