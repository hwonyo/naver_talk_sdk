from .base import Base
from .template import *


class Payload(Base):

    def __init__(self, user, **kwargs):
        super(Payload, self).__init__(**kwargs)

        self.user = user


class GenericPayload(Payload):
    """General Payload


    """

    def __init__(self, message, quick_reply=None, notification=False, **kwargs):
        """___init__ method.

        :param str Template | str message: Template to send
        :param Template.QuickReply | str quick_reply: quick_reply to send
        :param bool notification: set push alarm
        :param kwargs:
        """
        super(GenericPayload, self).__init__(**kwargs)

        self.event = 'send'
        self.options = {"notification": notification}
        if isinstance(message, str):
            message = TextContent(message)
        if quick_reply:
            if isinstance(quick_reply, list):
                quick_reply = QuickReply(quick_reply)
            message.quick_reply = quick_reply
        if isinstance(message, TextContent):
            self.text_content = message
        elif isinstance(message, ImageContent):
            self.image_content = message
        elif isinstance(message, CompositeContent):
            self.compositeContent = message
        else:
            raise ValueError("message type must be str or textContent or imageContent or compositeContent type !")


class ProfilePayload(Payload):
    """Porfile Payload

    """

    def __init__(self, field, agreements=None, **kwargs):
        super(ProfilePayload, self).__init__(**kwargs)

        self.event = 'profile'
        self.options = {
            'field': field,
            'agreements': agreements
        }

    @property
    def field(self):
        return self.options.get('field')

    @property
    def agreements(self):
        return self.options.get('agreements')


class ImageUploadPayload(Payload):

    def __init__(self, image_url, **kwargs):

        self.image_url = image_url