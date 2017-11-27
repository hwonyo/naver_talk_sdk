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
    def test_upload_image(self):
        responses.add(
            responses.POST,
            NaverTalkApi.DEFAULT_API_ENDPOINT,
            json={
                "success": True,
                "resultCode": "00",
                "imageId": "test-1234-image-id"
            },
            status=200
        )

        counter = mock.MagicMock()
        def test_callback(res, payload):
            self.assertEqual(res.result_code, "00")
            self.assertEqual(res.success, True)
            self.assertEqual(res.image_id, "test-1234-image-id")
            counter()

        self.tested.upload_image(
            'test_image_url.jpg',
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 1)