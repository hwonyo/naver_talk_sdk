#-*- encoding:utf-8 -*-
import json
import unittest
import responses
try:
    from unittest import mock
except:
    import mock


from nta import (
    NaverTalkApi
)
from nta.models import(
    ImageContent
)


class TestNaverTalkAPI(unittest.TestCase):
    def setUp(self):
        self.tested = NaverTalkApi('test_naver_talk_access_token')

    @responses.activate
    def test_send_image(self):
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
                    'imageContent': {
                        'imageUrl': 'test.jpg',
                    },
                    'options': {
                        'notification': False
                    }
                }
            )
            counter()

        self.tested.send(
            'test_user_id',
            ImageContent('test.jpg'),
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 1)

        counter2 = mock.MagicMock()
        def test_image_id_callback(res, payload):
            self.assertEqual(res.result_code, "00")
            self.assertEqual(res.success, True)
            self.assertEqual(
                payload,
                {
                    'event': 'send',
                    'user': 'test_user_id',
                    'imageContent': {
                        'imageId': '1234test',
                    },
                    'options': {
                        'notification': False
                    }
                }
            )
            counter2()

        self.tested.send(
            'test_user_id',
            ImageContent(image_id='1234test'),
            callback=test_image_id_callback
        )

        self.assertEqual(counter2.call_count, 1)