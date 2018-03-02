from .template import *
from .base import Base


class Payload(Base):
    """
    Base class of payload
    """
    def __init__(self, user, **kwargs):
        """ __init__ method.

         Args:
             - user: user_id
        """
        super(Payload, self).__init__(**kwargs)

        self.user = user


class GenericPayload(Payload):
    """
    General Payload
    For Send a message to users.
    """
    def __init__(self, message, quick_reply=None, notification=False, **kwargs):
        """__init__ method.

        Args:
            - message: str or Template.TextContent
            - quick_reply: list of buttons or Template.QuickReply
            - notification: boolean
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
    """
    Porfile Payload
    for request user's profile
    """
    def __init__(self, field, agreements=None, **kwargs):
        """ __init__ method.

        Args:
            - field: user profile information to get.
            - agreemetns: user profile information to get agreement.
        """
        super(ProfilePayload, self).__init__(**kwargs)

        self.event = 'profile'
        self.options = {
            'field': field,
            'agreements': agreements
        }



class ImageUploadPayload(Payload):
    """
    ImageUpload Payload
    for Upload image
    """
    def __init__(self, image_url, **kwargs):
        """__init__ method.

        Args:
            - image_url: full image url to convert
        """

        self.image_url = image_url

class ThreadPayload(Payload):
    """
    Thread Payload
    """
    def __init__(self, control, **kwargs):
        """__init__ method

        Args:
            - control: "takeThread" or "passThread"
        """
        super(ThreadPayload, self).__init__(**kwargs)
        self.event = 'handover'
        self.options = {
            'control': control,
        }
        if control == 'takeThread':
            self.options['metadata'] = ""
        if control == 'passThread':
            self.options['target_id'] = 1

class ActionPayload(Payload):
    """
    Action Payload for typing_on and typing_off
    """
    def __init__(self, action, **kwargs):
        """__init__ method.

        Args:
            - action: "typingOn" or "typingOff"
        """
        super(ActionPayload, self).__init__(**kwargs)

        self.event = 'action'
        self.options = {
            "action": action
        }


class PersistentMenuPayload(Base):
    def __init__(self, menus=None, **kwargs):
        super(PersistentMenuPayload, self).__init__(**kwargs)

        self.event = 'persistentMenu'
        self.menu_content = []
        if menus is not None:
            self.menu_content = [Menus(menus=menus)]