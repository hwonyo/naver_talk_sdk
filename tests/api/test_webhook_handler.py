#-*- encoding:utf8 -*-
import json
import responses
import unittest
try:
    from unittest import mock
except:
    import mock

from nta import (
    NaverTalkApi
)
from nta.models.events import  *
from nta.models import(
    NaverTalkResponse, GenericPayload
)


class TestNaverTalkApi(unittest.TestCase):
    def setUp(self):
        self.tested = NaverTalkApi('test_naver_talk_access_token')

    def test_open_event(self):
        event = {
            'event': 'open',
            'user': 'test_user_id',
            'options': {
                'inflow': 'list',
                'referer': 'https://example.com',
                'friend': True,
                'under14': False,
                'under19': False
            }
        }
        counter1 = mock.MagicMock()
        @self.tested.handle_open
        def test_handle_open(event):
            self.assertTrue(isinstance(event, OpenEvent))
            self.assertEqual('test_user_id', event.user_id)
            self.assertEqual('list', event.inflow)
            self.assertEqual('https://example.com', event.referer)
            self.assertFalse(event.under_14)
            self.assertFalse(event.under_19)
            self.assertTrue(event.friend)
            counter1()

        self.tested.webhook_handler(json.dumps(event))
        self.assertEqual(counter1.call_count, 1)

    def test_leave_event(self):
        event = {
            'event': 'leave',
            'user': 'test_user_id'
        }
        counter = mock.MagicMock()

        @self.tested.handle_leave
        def handle_leave(event):
            self.assertTrue(isinstance(event, LeaveEvent))
            self.assertEqual('test_user_id', event.user_id)
            counter()

        self.tested.webhook_handler(json.dumps(event))
        self.assertEqual(counter.call_count, 1)

    def test_friend_event(self):
        event = {
            'event': 'friend',
            'user': 'test_user_id',
            'options': {
                'set': 'on'
            }
        }

        counter = mock.MagicMock()

        @self.tested.handle_friend
        def handle_friend(event):
            self.assertTrue(isinstance(event, FriendEvent))
            self.assertEqual('test_user_id', event.user_id)
            self.assertTrue(event.set_on)
            counter()

        self.tested.webhook_handler(json.dumps(event))
        self.assertEqual(counter.call_count, 1)

    def test_send_event_text(self):
        event = {
            'event': 'send',
            'user': 'test_user_id',
            'textContent': {
                'text': 'test_text',
                'code': 'test_code',
                'inputType': 'typing'
            }
        }
        counter = mock.MagicMock()

        @self.tested.handle_send
        def send_handler(event):
            self.assertTrue(isinstance(event, SendEvent))
            self.assertEqual('test_user_id', event.user_id)
            self.assertEqual('test_text', event.text)
            self.assertEqual('test_code', event.code)
            self.assertEqual('typing', event.input_type)
            self.assertTrue(event.is_code)
            self.assertFalse(event.standby)
            counter()

        self.tested.webhook_handler(json.dumps(event))
        self.assertEqual(counter.call_count, 1)


    def test_send_event_image(self):
        event = {
            'event': 'send',
            'user': 'test_user_id',
            'imageContent': {
                'imageUrl': 'https://test.image.jpg'
            }
        }
        counter = mock.MagicMock()

        @self.tested.handle_send
        def send_handler(event):
            self.assertTrue(isinstance(event, SendEvent))
            self.assertEqual('test_user_id', event.user_id)
            self.assertEqual('https://test.image.jpg', event.image_url)
            self.assertIsNone(event.text)
            counter()

        self.tested.webhook_handler(json.dumps(event))
        self.assertEqual(counter.call_count, 1)

    def test_echo_event(self):
        event = {
            'event': 'echo',
            'echoedEvent': 'send',
            'user': 'test_user_id',
            'partner': 'testyo',
            'imageContent': {
                'imageUrl': 'https://example_image.png'
            },
            'textContent':{
                'text':'text_from_test'
            },
            'compositeContent': {
                'compositeList':[]
            },
            'options': {
                'mobile': False
            }
        }
        counter = mock.MagicMock()

        @self.tested.handle_echo
        def echo_handler(event):
            self.assertTrue(isinstance(event, EchoEvent))
            self.assertEqual('test_user_id', event.user_id)
            self.assertEqual('send', event.echoed_event)
            self.assertEqual({'text':'text_from_test'}, event.text_content)
            self.assertEqual({'composite_list':[]}, event.composite_content)
            self.assertEqual({'image_url': 'https://example_image.png'}, event.image_content)
            self.assertFalse(event.mobile)
            counter()

        self.tested.webhook_handler(json.dumps(event))
        self.assertEqual(counter.call_count, 1)

    def test_profile_event(self):
        event = {
            'event': 'profile',
            'user': 'test_user_id',
            'options': {
                'nickname': 'test_won_yo',
                'cellphone': '01012345678',
                'address': {
                    'roadAddr': 'Seoul'
                },
                'result': 'SUCCESS'
            }
        }
        counter = mock.MagicMock()

        @self.tested.handle_profile
        def profile_handler(event):
            self.assertTrue(isinstance(event, ProfileEvent))
            self.assertEqual('test_user_id', event.user_id)
            self.assertEqual('test_won_yo', event.nickname)
            self.assertEqual('01012345678', event.cellphone)
            self.assertEqual({'road_addr': 'Seoul'}, event.address)
            self.assertEqual('SUCCESS', event.result)
            counter()

        self.tested.webhook_handler(json.dumps(event))
        self.assertEqual(counter.call_count, 1)

    def test_pay_complete_event(self):
        event = {
            'event': 'pay_complete',
            'user': 'test_user_id',
            'options': {
                'paymentResult': {
                    'code': 'Success',
                    'paymentId': 'test-payment-id',
                    'merchantPayKey': 'test_merchant-pay-key',
                    'merchantUserKey': 'test-merchant-user-key'
                }
            }
        }
        counter = mock.MagicMock()

        @self.tested.handle_pay_complete
        def pay_complete_handler(event):
            self.assertTrue(isinstance(event, PayCompleteEvent))
            self.assertEqual('Success', event.code)
            self.assertEqual('test-payment-id', event.payment_id)
            self.assertEqual('test_merchant-pay-key', event.merchant_pay_key)
            self.assertEqual('test-merchant-user-key', event.merchant_user_key)
            self.assertIsNone(event.message)
            counter()

        self.tested.webhook_handler(json.dumps(event))
        self.assertEqual(counter.call_count, 1)


    def test_pay_confirm_event(self):
        event = {
            'event': 'pay_confirm',
            'user': 'test_user_id',
            'options': {
                'paymentConfirmResult': {
                    'code': 'Success',
                    'message': 'test_message',
                    'paymentId': 'test-payment-id',
                    'detail': {}
                }
            }
        }
        counter = mock.MagicMock()

        @self.tested.handle_pay_confirm
        def pay_complete_handler(event):
            self.assertTrue(isinstance(event, PayConfirmEvent))
            self.assertEqual('Success', event.code)
            self.assertEqual('test_message', event.message)
            self.assertEqual('test-payment-id', event.payment_id)
            self.assertEqual({}, event.detail)
            counter()

        self.tested.webhook_handler(json.dumps(event))
        self.assertEqual(counter.call_count, 1)

    def test_handover_event(self):
        event = {
            "event": "handover",
            "user": "test_user",
            "partner": "wc1234",
            "options": {
                "control": "passThread",
                "metadata": "{\"managerNickname\":\"파트너닉네임\",\"autoEnd\":false}"
            }
        }
        counter = mock.MagicMock()

        @self.tested.handle_handover
        def hanover_event_handler(event):
            self.assertTrue(isinstance(event, HandOverEvent))
            self.assertEqual('test_user', event.user_id)
            self.assertEqual('passThread', event.control)
            self.assertEqual("{\"managerNickname\":\"파트너닉네임\",\"autoEnd\":false}", event.metadata)
            counter()

        self.tested.webhook_handler(json.dumps(event))
        self.assertEqual(counter.call_count, 1)

    def test_standby_true(self):
        event = {
            'standby': True,
            'event': 'send',
            'user': 'test_user_id',
            'textContent': {
                'text': 'test_text',
                'code': 'test_code',
                'inputType': 'typing'
            },
            'options': {
                'mobile': False
            }
        }
        counter = mock.MagicMock()

        @self.tested.handle_send
        def send_handler(event):
            self.assertTrue(event.standby)
            counter()

        self.tested.webhook_handler(json.dumps(event))
        self.assertEqual(counter.call_count, 1)

    @responses.activate
    def test_after_send(self):
        responses.add(
            responses.POST,
            self.tested.DEFAULT_API_ENDPOINT,
            json={
                'success': True,
                'resultCode': '00'
            },
            status=200
        )

        counter = mock.MagicMock()
        @self.tested.after_send
        def after_send_handler(res, payload):
            self.assertTrue(isinstance(res, NaverTalkResponse))
            self.assertTrue(isinstance(payload, GenericPayload))
            counter()

        self.tested.send('test_user_id', 'test_text')
        self.assertEqual(counter.call_count, 1)

    def test_before_proccess(self):
        event = {
            'event': 'leave',
            'user': 'test_user_id'
        }

        counter = mock.MagicMock()

        @self.tested.before_proccess
        def before_proccess_handler(event):
            counter()

        self.tested.webhook_handler(json.dumps(event))
        self.assertEqual(counter.call_count, 1)

    def test_callback(self):
        event = {
            'event': 'send',
            'user': 'test_user_id',
            'textContent': {
                'text': 'test_text',
                'code': 'test_code',
                'inputType': 'typing'
            }
        }

        counter1 = mock.MagicMock()
        @self.tested.callback
        def default_callback(event):
            self.assertEqual('test_code', event.code)
            counter1()

        @self.tested.handle_send
        def send_event_handler(event):
            if event.is_code:
                return
            counter1()

        self.tested.webhook_handler(json.dumps(event))
        self.assertEqual(counter1.call_count, 1)

        event2 = {
            'event': 'send',
            'user': 'test_user_id',
            'textContent': {
                'text': 'test_text',
                'code': 'Hello my name is wonyo',
                'inputType': 'typing'
            }
        }

        counter2 = mock.MagicMock()
        @self.tested.callback([('(^Hello).*')])
        def callback_handler(event):
            self.assertEqual('Hello my name is wonyo', event.code)
            counter2()

        self.tested.webhook_handler(json.dumps(event2))
        self.assertEqual(counter1.call_count, 1)

        event3 = {
            'event': 'send',
            'user': 'test_user_id',
            'textContent': {
                'text': 'test_text',
                'code': '1',
                'inputType': 'typing'
            }
        }

        counter3 = mock.MagicMock()
        @self.tested.callback(['1', '2', '3'])
        def callback_handler(event):
            self.assertEqual('1', event.code)
            counter3()

        self.tested.webhook_handler(json.dumps(event3))
        self.assertEqual(counter3.call_count, 1)

    def test_unknown_event(self):
        event = {
            'event': 'unknown'
        }
        counter = mock.MagicMock()

        @self.tested.handle_open
        def handle_open(event):
            counter()

        @self.tested.handle_leave
        def handle_open(event):
            counter()

        @self.tested.handle_send
        def handle_open(event):
            counter()

        @self.tested.handle_friend
        def handle_open(event):
            counter()

        @self.tested.handle_echo
        def handle_open(event):
            counter()

        @self.tested.handle_pay_complete
        def handle_open(event):
            counter()

        @self.tested.handle_pay_confirm
        def handle_open(event):
            counter()

        @self.tested.handle_profile
        def handle_open(event):
            counter()


        self.tested.webhook_handler(json.dumps(event))
        self.assertEqual(counter.call_count, 0)



if __name__ == '__main__':
    unittest.main()