"""
    nta
    ~~~

    :copyright: (c) 2017 by Wonyo Hwang. hollal0726@gmail.com
    :license: MIT, see LICENSE for more details.

"""
import re
import requests
import json

from .exceptions import NaverTalkApiError, NaverTalkApiConnectionError
from .models.responses import NaverTalkResponse, NaverTalkImageResponse
from .models.payload import (
    ProfilePayload, GenericPayload, ImageUploadPayload, ThreadPayload, ActionPayload,
    PersistentMenuPayload
)
from .models.events import *

from .utils import LOGGER, PY3, _byteify


class WebhookParser(object):
    """Webhook Parser.
    WebhookParser for parsing json request from navertalk.
    It returns parsed data in an Event instance
    with snake case attributes.
    """

    def parse(self, req):
        """
        Parse webhook request
        and change into the Event instance

        Args:
            - req: request body from navertalk

        Returns:
            - event: Event instance in mdoels.events
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
        elif event_type == 'handover':
            event = HandOverEvent.new_from_json_dict(req_json)
        else:
            LOGGER.warn('Unknown event type: %s' % event_type)
            event = None

        return event


class NaverTalkApi(object):
    """NaverTalk Webhook Agent"""

    DEFAULT_API_ENDPOINT = 'https://gw.talk.naver.com/chatbot/v1/event'

    def __init__(self, naver_talk_access_token, endpoint=DEFAULT_API_ENDPOINT, **options):
        """ __init__ method.

        Args:
            - naver_talk_access_token: issued access_token
            - endpoint: endpoint to post request
        """

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
        """
        Call handler for event matched by name.

        Args:
              - name: event name
              - event: event to be handled
        """
        if name in self._webhook_handlers:
            func = self._webhook_handlers[name]
            func(event)
        else:
            LOGGER.warn('No matching %s event handler' % name)

    def webhook_handler(self, req):
        """Handle webhook.

        :param req: Webhook request body (as text)
        """
        event = self.parser.parse(req)
        if event is not None:
            if self._before_process:
                self._before_process(event)
            if isinstance(event, SendEvent):
                if event.is_code:
                    _matched_callbacks = self.get_code_callbacks(event.code)
                    for callback in _matched_callbacks:
                        callback(event)
            name = event.event
            self._call_handler(name, event)

    def send(self, user_id, message, quick_reply=None, notification=False, callback=None):
        """
        Send a message to user_id with quick_reply or not.
        If notification True, push alarm occurred on user's phone.
        Callback function is invoked after sending the message to user is Success.

        Args:
            - user_id: Navertalk user_id.
            - message: Instances in Template or str are allowed
            - quick_reply: add quickReply end of contents.
            - notification: on push alarm if True
            - callback: Do something after send a message
        """
        if not PY3:
            if isinstance(message, unicode):
                message = _byteify(message)

        payload = GenericPayload(
            user=user_id,
            message=message,
            quick_reply=quick_reply,
            notification=notification
        )

        self._send(payload, callback=callback)

    def _send(self, payload, callback=None, response_form=NaverTalkResponse):
        """
        Request Post to Navertalktalk.
        """
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
        """
        Request user's profile with user_id, and agreement fields.

        Args:
            - user_id: target user's id
            - field: target user info nickname|cellphone|addreess
            - agreements: list of user's info nickname|cellphone|addreess
        """
        payload = ProfilePayload(
            user=user_id,
            field=field,
            agreements=agreements
        )

        self._send(payload, callback=callback)

    def upload_image(self, image_url, callback=None):
        """
        Upload image with url to navertalk and recieve an Image Id.

        Args:
            - image_url: imaegUrl to imageId
            - callback: function callback after image upload request.
                        the function will recieve models.NaverTalkImageResponse and payload.
        """
        payload = ImageUploadPayload(
            image_url
        )

        self._send(payload, callback=callback, response_form=NaverTalkImageResponse)

    def take_thread(self, user_id, callback=None):
        """
        take thread from partner for a user's conversation with user_id

         Args:
             - user_id: target user
             - callback: function callback
        """
        payload = ThreadPayload(
            user=user_id,
            control="takeThread"
        )

        self._send(payload, callback=callback)

    def pass_thread(self, user_id, callback=None):
        """
        pass thread to partner for a user's conversation with user_id

        Args:
             - user_id: target user
             - callback: function callback
        """
        payload = ThreadPayload(
            user=user_id,
            control="passThread"
        )

        self._send(payload, callback=callback)

    def typing_on(self, user_id, callback=None):
        """
        make typing_on action on

        Args:
             - user_id: target user
             - callback: function callback
        """
        payload = ActionPayload(
            user=user_id,
            action="typingOn"
        )

        self._send(payload, callback=callback)

    def typing_off(self, user_id, callback=None):
        """
        make typing_on action off

        Args:
             - user_id: target user
             - callback: function callback
        """
        payload = ActionPayload(
            user=user_id,
            action="typingOff"
        )

        self._send(payload, callback=callback)

    def persistent_menu(self, menus=None, callback=None):
        """
        enroll persistent menu.

        Args:
            - menus: List of Buttons
        """
        payload = PersistentMenuPayload(menus)

        self._send(payload, callback=callback)

    """
    Decorators
    for Handling each events.
    """
    def handle_open(self, func):
        """open decorator"""
        self._webhook_handlers['open'] = func

    def handle_send(self, func):
        """send decorator"""
        self._webhook_handlers['send'] = func

    def handle_leave(self, func):
        """leave decorator"""
        self._webhook_handlers['leave'] = func

    def handle_friend(self, func):
        """friend decorator"""
        self._webhook_handlers['friend'] = func

    def handle_profile(self, func):
        """profile decorator"""
        self._webhook_handlers['profile'] = func

    def handle_pay_complete(self, func):
        """payComplete decorator"""
        self._webhook_handlers['pay_complete'] = func

    def handle_pay_confirm(self, func):
        """payConfirm decorator"""
        self._webhook_handlers['pay_confirm'] = func

    def handle_echo(self, func):
        """echo decorator"""
        self._webhook_handlers['echo'] = func

    def handle_handover(self, func):
        """handover decorator"""
        self._webhook_handlers['handover'] = func

    def before_proccess(self, func):
        """before_proccess decorator.
        Decorated function which is invoked ahead of all event handlers.
        """
        self._before_process = func

    def after_send(self, func):
        """after_send decorator.
        Decorated function will be invoked after sending each message.
        """
        self._after_send = func

    def callback(self, *args):
        """
        Callback wrapper for handling code value.
        Regular expression can be used for mathching with code value.

        Args: callbale or list of target code values
        """
        def wrapper(func):
            if not isinstance(args[0], list):
                raise ValueError("Callback params must be List")
            for arg in args[0]:
                self._button_callbacks[arg] = func
                self._button_callbacks_key_regex[arg] = re.compile(arg + '$')

        if not callable(args[0]):
            return wrapper

        self._default_button_callback = args[0]

    def get_code_callbacks(self, code):
        """
        find callback handlers matched by code value with regular expression.

        Args:
            - code: code value from a button.

        Return:
            - callbacks: function callbacaks matched by code value
        """
        callbacks = []
        for key in self._button_callbacks.keys():
            if self._button_callbacks_key_regex[key].match(code):
                callbacks.append(self._button_callbacks[key])

        if not callbacks:
            if self._default_button_callback is not None:
                callbacks.append(self._default_button_callback)
        return callbacks

    def __error_check(self, response):
        """
        check error from navertalk.
        When recieved success: false, raise NaverTalkApiError.
        """
        if not response.success:
            raise NaverTalkApiError(response)