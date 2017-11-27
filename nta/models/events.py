#-*- encoding:utf-8 -*-
from .base import Base

class Event(Base):
    def __init__(self, user, **kwargs):
        super(Event, self).__init__(**kwargs)

        self.user = user

    @property
    def user_id(self):
        return self.user



class OpenEvent(Event):
    def __init__(self, options, **kwargs):
        super(OpenEvent, self).__init__(**kwargs)

        self.event = 'open'
        self.options = options

    @property
    def inflow(self):
        return self.options.get('inflow')

    @property
    def referer(self):
        return self.options.get('referer')

    @property
    def friend(self):
        return self.options.get('friend')

    @property
    def under_14(self):
        return self.options.get('under_14')

    @property
    def under_19(self):
        return self.options.get('under_19')


class LeaveEvent(Event):
    def __init__(self, **kwargs):
        super(LeaveEvent, self).__init__(**kwargs)

        self.event = 'leave'


class FriendEvent(Event):
    def __init__(self, options, **kwargs):
        super(FriendEvent, self).__init__(**kwargs)

        self.event = 'friend'
        self.options = options

    @property
    def set_on(self):
        return self.options.get('set') == 'on'


class SendEvent(Event):
    def __init__(self, text_content=None, image_content=None, **kwargs):
        super(SendEvent, self).__init__(**kwargs)

        self.event = 'send'
        self.text_content = {}
        if text_content:
            self.text_content = text_content
        self.image_content = {}
        if image_content:
            self.image_content = image_content

    @property
    def text(self):
        return self.text_content.get('text')

    @property
    def code(self):
        return self.text_content.get('code')

    @property
    def input_type(self):
        return self.text_content.get('input_type')

    @property
    def is_code(self):
        return self.text_content.get('code') is not None

    @property
    def image_url(self):
        return self.image_content.get('image_url')


class EchoEvent(Event):
    def __init__(self, echoed_event, **kwargs):
        super(EchoEvent, self).__init__(**kwargs)

        self.event = 'echo'
        self.echoed_event = echoed_event


class PayCompleteEvent(Event):
    def __init__(self, options, **kwargs):
        super(PayCompleteEvent, self).__init__(**kwargs)

        self.event = 'pay_complete'
        self.options = options

    @property
    def payment_result(self):
        return self.options.get('payment_result', {})

    @property
    def code(self):
        return self.payment_result.get('code')

    @property
    def payment_id(self):
        return self.payment_result.get('payment_id')

    @property
    def merchant_pay_key(self):
        return self.payment_result.get('merchant_pay_key')

    @property
    def merchant_user_key(self):
        return self.payment_result.get('merchant_user_key')

    @property
    def message(self):
        return self.payment_result.get('message')


class PayConfirmEvent(Event):
    def __init__(self, options, **kwargs):
        super(PayConfirmEvent, self).__init__(**kwargs)

        self.type = 'pay_confirm'
        self.options = options

    @property
    def payment_confirm_result(self):
        return self.options.get('payment_confirm_result', {})

    @property
    def code(self):
        return self.payment_confirm_result.get('code')

    @property
    def message(self):
        return self.payment_confirm_result.get('message')

    @property
    def payment_id(self):
        return self.payment_confirm_result.get('payment_id')

    @property
    def detail(self):
        """
        네이버페이 간편결제 결제승인 API 응답본문의 detail 필드를 그대로 반환.
        """
        return self.payment_confirm_result.get('detail')


class ProfileEvent(Event):
    def __init__(self, options, **kwargs):
        super(ProfileEvent, self).__init__(**kwargs)

        self.event = 'profile'
        self.options = options

    @property
    def result(self):
        return self.options.get('result')

    @property
    def nickname(self):
        return self.options.get('nickname')

    @property
    def cellphone(self):
        return self.options.get('cellphone')

    @property
    def address(self):
        return self.options.get('address')