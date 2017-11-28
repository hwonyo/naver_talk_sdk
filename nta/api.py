#-*- unicode:utf8 -*-
import re
import requests
import json

from .exceptions import NaverTalkApiError, NaverTalkApiConnectionError
from .models.responses import NaverTalkResponse, NaverTalkImageResponse
from .models.payload import ProfilePayload, GenericPayload, ImageUploadPayload
from .models.events import *

from .utils import LOGGER, PY3, _byteify


class WebhookParser(object):
    """Webhook Parser."""

    def parse(self, req):
        """Parse webhook request body as text.

        :param str req: Webhook request body (as text)
        :rtype: Event
        :return:
        """
        if not PY3:
            req_json = json.loads(req, object_hook=_byteify)
        else:
            req_json = json.loads(req)

        event_type = req_json['event']
        if event_type == 'open':
            event = OpenEvent.new_from_json_dict(req_json)
        elif event_type == 'send':
            event = SendEvent.new_from_json_dict(req_json)
        elif event_type == 'leave':
            event = LeaveEvent.new_from_json_dict(req_json)
        elif event_type == 'friend':
            event = FriendEvent.new_from_json_dict(req_json)
        elif event_type == 'echo':
            event = EchoEvent.new_from_json_dict(req_json)
        elif event_type == 'pay_complete':
            event = PayCompleteEvent.new_from_json_dict(req_json)
        elif event_type == 'pay_confirm':
            event = PayConfirmEvent.new_from_json_dict(req_json)
        elif event_type == 'profile':
            event = ProfileEvent.new_from_json_dict(req_json)
        else:
            LOGGER.warn('Unknown event type: %s' % event_type)
            event = None

        return event


class NaverTalkApi(object):
    """NaverTalk Webhook Agent"""

    DEFAULT_API_ENDPOINT = 'https://gw.talk.naver.com/chatbot/v1/event'

    def __init__(self, naver_talk_access_token, endpoint=DEFAULT_API_ENDPOINT, **options):

        self._endpoint = endpoint
        self._headers = {
            'Content-type': 'application/json;charset=UTF-8',
            'Authorization': naver_talk_access_token
        }
        self.parser = WebhookParser()

    _webhook_handlers = {}
    _button_callbacks = {}
    _button_callbacks_key_regex = {}
    _default_button_callback = None
    _before_process = None
    _after_send = None

    def _call_handler(self, name, event):
        if name in self._webhook_handlers:
            func = self._webhook_handlers[name]
            func(event)
        else:
            LOGGER.warn('No matching %s event handler' % name)

    def webhook_handler(self, data):
        """Handle webhook.

        :param str data: Webhook request body (as text)
        """
        event = self.parser.parse(data)
        if event is not None:
            if self._before_process:
                self._before_process(event)
            if isinstance(event, OpenEvent):
                self._call_handler('open', event)
            elif isinstance(event, SendEvent):
                if event.is_code:
                    _matched_callbacks = self.get_code_callbacks(event)
                    for callback in _matched_callbacks:
                        callback(event)
                self._call_handler('send', event)
            elif isinstance(event, LeaveEvent):
                self._call_handler('leave', event)
            elif isinstance(event, FriendEvent):
                self._call_handler('friend', event)
            elif isinstance(event, ProfileEvent):
                self._call_handler('profile', event)
            elif isinstance(event, PayCompleteEvent):
                self._call_handler('pay_complete', event)
            elif isinstance(event, PayConfirmEvent):
                self._call_handler('pay_confirm', event)
            elif isinstance(event, EchoEvent):
                self._call_handler('echo', event)

    def send(self, user_id, message, quick_replies=None, notification=False, callback=None):
        """

        :param user_id:
        :param message:
        :param quick_replies:
        :param notification:
        :return:
        """
        if not PY3:
            if isinstance(message, unicode):
                message = _byteify(message)

        payload = GenericPayload(
            user=user_id,
            message=message,
            quick_replies=quick_replies,
            notification=notification
        )

        return self._send(payload, callback=callback)

    def _send(self, payload, callback=None, response_form=NaverTalkResponse):
        data = payload.as_json_string()
        r = requests.post(self._endpoint,
                          data=data,
                          headers=self._headers)

        if r.status_code != requests.codes.ok:
            raise NaverTalkApiConnectionError(r)

        res = response_form.new_from_json_dict(r.json())
        self.__error_check(res)

        if callback is not None:
            callback(res, payload)

        if self._after_send:
            self._after_send(res, payload)


    def request_profile(self, user_id, field, agreements=None, callback=None):
        """Handle Profile Request

        :param str user_id: Target user's id
        :param str field: Target user info nickname|cellphone|addreess
        :param list agreements: Target agreement user info nickname|cellphone|addreess
        :rtype: None
        :return:
        """
        payload = ProfilePayload(
            user=user_id,
            field=field,
            agreements=agreements
        )

        return self._send(payload, callback=callback)


    def upload_image(self, image_url, callback=None):
        """Handle Image Upload

        :param str image_url: imaegUrl to imageId
        :param func callback: function callback after image upload request
        :func will recieve NaverTalkImageResponse and payload
        """
        payload = ImageUploadPayload(
            image_url
        )

        return self._send(payload, callback=callback, response_form=NaverTalkImageResponse)

    """
    decorations
    """
    def handle_open(self, func):
        self._webhook_handlers['open'] = func

    def handle_send(self, func):
        self._webhook_handlers['send'] = func

    def handle_leave(self, func):
        self._webhook_handlers['leave'] = func

    def handle_friend(self, func):
        self._webhook_handlers['friend'] = func

    def handle_profile(self, func):
        self._webhook_handlers['profile'] = func

    def handle_pay_complete(self, func):
        self._webhook_handlers['pay_complete'] = func

    def handle_pay_confirm(self, func):
        self._webhook_handlers['pay_confirm'] = func

    def handle_echo(self, func):
        self._webhook_handlers['echo'] = func

    def before_proccess(self, func):
        """before_proccess decorator.

        Function with event attr.
        :param func:
        :return:
        """
        self._before_process = func

    def after_send(self, func):
        """after_send decorator.

        Function with response and payload
        :param func:
        :return:
        """
        self._after_send = func

    def callback(self, *args):
        def wrapper(func):
            if not isinstance(args[0], list):
                raise ValueError("Callback params must be List")
            for arg in args[0]:
                self._button_callbacks[arg] = func

        if not callable(args[0]):
            return wrapper

        self._default_button_callback = args[0]


    def get_code_callbacks(self, event):
        callbacks = []
        for key in self._button_callbacks.keys():
            if key not in self._button_callbacks_key_regex:
                self._button_callbacks_key_regex[key] = re.compile(key + '$')
            if self._button_callbacks_key_regex[key].match(event.code):
                callbacks.append(self._button_callbacks[key])

        if not callbacks:
            if self._default_button_callback is not None:
                callbacks.append(self._default_button_callback)
        return callbacks


    def __error_check(self, response):
        if not response.success:
            raise NaverTalkApiError(response)