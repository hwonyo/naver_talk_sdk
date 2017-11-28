#-*- encoding:utf8 -*-
from __future__ import unicode_literals, absolute_import

import unittest
import responses


from nta import (
    NaverTalkApi
)
from nta.exceptions import (
    NaverTalkApiError,
    NaverTalkApiConnectionError
)


class TestNaverTalkApi(unittest.TestCase):
    def setUp(self):
        self.tested = NaverTalkApi('test_naver_talk_access_token')

    @responses.activate
    def test_connection_error_handle(self):
        responses.add(
            responses.POST,
            NaverTalkApi.DEFAULT_API_ENDPOINT,
            json={
                "message": "Internal Server Error"
            },
            status=500
        )

        try:
            self.tested.send('test_id', 'test message')
        except NaverTalkApiConnectionError as e:
            self.assertEqual(e.status_code, 500)
            self.assertEqual(e.message, '{"message": "Internal Server Error"}')


    @responses.activate
    def test_error_with_detail_handle(self):
        responses.add(
            responses.POST,
            NaverTalkApi.DEFAULT_API_ENDPOINT,
            json={
                'success': False,
                'resultCode': "02",
                'resultMessage': "request json 문자열 파싱 에러"
            },
            status=200
        )

        try:
            self.tested.send('test_id', 'test message')
        except NaverTalkApiError as e:
            self.assertEqual(e.status_code, 200)
            self.assertEqual(e.result_code, "02")
            self.assertEqual(e.message, 'request json 문자열 파싱 에러')

    @responses.activate
    def test_error_handle_get_user_profile(self):
        responses.add(
            responses.POST,
            NaverTalkApi.DEFAULT_API_ENDPOINT,
            json={
                'success': False,
                'resultCode': "02",
                'resultMessage': "request json 문자열 파싱 에러"
            },
            status=200
        )

        try:
            self.tested.request_profile('test_id', 'nickname')
        except NaverTalkApiError as e:
            self.assertEqual(e.status_code, 200)
            self.assertEqual(e.result_code, "02")
            self.assertEqual(e.message, 'request json 문자열 파싱 에러')

    @responses.activate
    def test_error_handle_upload_image_url(self):
        responses.add(
            responses.POST,
            NaverTalkApi.DEFAULT_API_ENDPOINT,
            json={
                'success': False,
                'resultCode': "IMG-99",
                'resultMessage': "이미지 업로드 중 에러"
            },
            status=200
        )

        try:
            self.tested.upload_image('https://example.com/test.jpg')
        except NaverTalkApiError as e:
            self.assertEqual(e.status_code, 200)
            self.assertEqual(e.result_code, "IMG-99")
            self.assertEqual(e.message, "이미지 업로드 중 에러")

    def test_callback_error(self):
        with self.assertRaises(ValueError):
            @self.tested.callback('Hello')
            def callback_test(event):
                pass


if __name__ == '__main__':
    unittest.main()