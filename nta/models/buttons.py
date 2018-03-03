from .base import Base


class Buttons(Base):
    """Base class of Buttons."""
    @staticmethod
    def convert_shortcut_buttons(items):
        """
        support shortcut buttons.
        EX) [{'type':'TEXT', 'title':'text', 'value':'PAYLOAD'}]
        """
        if items is not None and isinstance(items, list):
            result = []
            for item in items:
                if isinstance(item, Buttons):
                    result.append(item)
                elif isinstance(item, dict):
                    if item.get('type') in ['TEXT', 'LINK', 'OPTION', 'PAY']:
                        type = item.get('type')
                        title = item.get('title')
                        value = item.get('value', item.get('url', item.get('code', item.get('buttons'))))

                        if type == 'TEXT':
                            result.append(ButtonText(title=title, code=value))
                        elif type == 'LINK':
                            moburl = item.get('mobile_url')
                            result.append(ButtonLink(title=title, url=value, mobile_url=moburl))
                        elif type == 'OPTION':
                            result.append(ButtonOption(title=title, button_list=value))
                        elif type == 'PAY':
                            result.append(ButtonPay(payment_info=value))

                    else:
                        raise ValueError('Invalid button type')
                else:
                    raise ValueError('Invalid buttons variables')
            return result
        else:
            return items


class ButtonText(Buttons):
    """
    ButtonText for text button to use quickReply and Composite buttons.
    Invoke Send Event with code value from navertalk to server when user clicks the button.
    """
    def __init__(self, title, code=None, **kwargs):
        """ __init__ method.

        :param title: exposed text on the button
        :param code:  enclosed value under the button
        :param kwargs:
        """
        super(ButtonText, self).__init__(**kwargs)

        self.type = "TEXT"
        self.data = {
            "title": title
        }
        if code:
            self.data['code'] = code


class ButtonLink(Buttons):
    """
    ButtonLink for link button to use quickReply and Composite button.
    Links to url address when user click the button.
    """
    def __init__(self, title, url, mobile_url=None, webview=False, webview_title=None, webview_height=None, **kwargs):
        """ __init__ method.

        :param title: exposed text on the button
        :param url: default linked url
        :param mobile_url: linked url on mobile device
        :param kwargs:
        """
        super(ButtonLink, self).__init__(**kwargs)

        self.type = "LINK"
        self.data = {
            "title":title,
            "url":url,
            "mobile_url": mobile_url
        }
        if webview:
            self.data['mobile_target'] = 'webview'
            self.data['mobile_target_attr'] = {
                "webview_title": webview_title,
                "webview_height": webview_height
            }


class ButtonOption(Buttons):
    """
    ButtonOption for option button in Composite button.
    ButtonOption contains the other buttons.
    """
    def __init__(self, title, button_list, **kwargs):
        """ __init___ method.

        :param title: exposed text on the button
        :param button_list: Contained butons list. List of Template.Button
        :param kwargs:
        """
        super(ButtonOption, self).__init__(**kwargs)

        if not isinstance(button_list, list):
            button_list = [button_list]
        self.type = "OPTION"
        self.data = {
            "title":title,
            "button_list": self.convert_shortcut_buttons(button_list)
        }


class ButtonPay(Buttons):
    """
    ButtonPay for pay button in quickReply and Composite button.
    User can Proceed payment when clicks the button.
    """
    def __init__(self, payment_info, **kwargs):
        """ __init__ method.

        :param payment_info: Template.PaymentInfo Instance
        :param kwargs:
        """
        super(ButtonPay, self).__init__(**kwargs)

        self.type = 'PAY'
        self.data = {
            'payment_info': payment_info
        }


class ButtonNested(Buttons):
    def __init__(self, title, menus, **kwargs):
        super(ButtonNested, self).__init__(**kwargs)

        self.type = 'NESTED'
        self.data = {
            'title': title,
            'menus': menus
        }


class ButtonTime(Buttons):
    def __init__(self, title, code, **kwargs):
        super(ButtonTime, self).__init__(**kwargs)

        self.type = 'TIME'
        self.data = {
            'title': title,
            'code': code
        }