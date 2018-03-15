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
    CompositeContent, Composite, ElementData, ElementList,
    ButtonText, ButtonLink, ButtonCalendar, QuickReply
)


class TestNaverTalkAPI(unittest.TestCase):
    def setUp(self):
        self.tested = NaverTalkApi('test_naver_talk_access_token')

    @responses.activate
    def test_send_composite(self):
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
                payload.as_json_dict(),
                {
                    'event': 'send',
                    'user': 'test_user_id',
                    'compositeContent': {
                        'compositeList': [
                            {
                                'title': 'test_title',
                                'description': 'test_descript',
                                'image': {
                                    'imageUrl': 'test_image'
                                },
                                'elementList':{
                                    'type': 'LIST',
                                    'data': [
                                        {
                                            'title': 'test_ed_title',
                                            'description': 'test_ed_descript',
                                            'subDescription': 'test_ed_subdescript',
                                            'image': {
                                                'imageUrl': 'test_ed_image'
                                            },
                                            'button':{
                                                'type': 'TEXT',
                                                'data': {
                                                    'title': 'test'
                                                }
                                            }
                                        }
                                    ]

                                },
                                'buttonList': None
                            }
                        ]
                    },
                    'options': {
                        'notification': False
                    }
                }
            )
            counter()


        self.tested.send(
            'test_user_id',
            message=CompositeContent(
                composite_list=[
                    Composite(
                        title='test_title',
                        description='test_descript',
                        image='test_image',
                        element_list=ElementList([
                            ElementData(
                                title='test_ed_title',
                                description='test_ed_descript',
                                sub_description='test_ed_subdescript',
                                image='test_ed_image',
                                button=ButtonText('test')
                            )
                        ])
                    )
                ]
            ),
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 1)

    @responses.activate
    def test_send_composite_with_quick_reply(self):
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
                payload.as_json_dict(),
                {
                    'event': 'send',
                    'user': 'test_user_id',
                    'compositeContent': {
                        'compositeList': [
                            {
                                'title': 'test_title',
                                'description': None,
                                'elementList': None,
                                'buttonList': None
                            }
                        ],
                        'quickReply': {
                            'buttonList': [{
                                'data': {
                                    'code': 'PAYLOAD',
                                    'title': 'text'},
                                'type': 'TEXT'},
                                {
                                    'data': {
                                        'mobileUrl': None,
                                        'title': 'text',
                                        'url': 'PAYLOAD'},
                                    'type': 'LINK'}]}

                    },
                    'options': {
                        'notification': False
                    }
                }
            )
            counter()

        self.tested.send(
            'test_user_id',
            message=CompositeContent(
                composite_list=[
                    Composite(
                        title='test_title'
                    )
                ]
            ),
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
            message=CompositeContent(
                composite_list=[
                    Composite(
                        title='test_title'
                    )
                ],
                quick_reply=[
                        ButtonText('text', 'PAYLOAD'),
                        ButtonLink('text', 'PAYLOAD')
                ]
            ),
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 2)

    @responses.activate
    def test_composite_with_calendar(self):
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
            target = {
                "event": "send",
                "user": "test_user_id",
                "compositeContent": {
                    "compositeList": [
                        {
                            "title": "톡톡 레스토랑",
                            "description": "파스타가 맛있는집",
                            'elementList': None,
                            "buttonList": [
                                {
                                    "type": "CALENDAR",
                                    "data": {
                                        "title": "방문 날짜 선택하기",
                                        "code": "code_for_your_bot",
                                        "options": {
                                            "calendar": {
                                                "placeholder": "방문 날짜를 선택해주세요.",
                                                "start": "20180301",
                                                "end": "20180430",
                                                "disables": "1,20180309,20180315-20180316"
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                },
                'options': {
                    'notification': False
                }
            }
            self.assertEqual(target, payload.as_json_dict())
            counter()

        self.tested.send(
            "test_user_id",
            message=CompositeContent(
                composite_list=[
                    Composite(
                        title= "톡톡 레스토랑",
                        description="파스타가 맛있는집",
                        button_list=[
                            ButtonCalendar(
                                title="방문 날짜 선택하기",
                                code="code_for_your_bot",
                                placeholder="방문 날짜를 선택해주세요.",
                                start="20180301",
                                end="20180430",
                                disables="1,20180309,20180315-20180316"
                            )
                        ]
                    )

                ]
            ),
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 1)