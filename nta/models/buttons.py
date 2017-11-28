#-*- encoding:utf-8 -8-
from .base import Base


class Buttons(Base):
    @staticmethod
    def convert_shortcut_buttons(items):
        """
        support shortcut buttons [{'type':'TEXT', 'title':'text', 'value':'PAYLOAD'}]
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
    def __init__(self, title, code=None, **kwargs):
        super(ButtonText, self).__init__(**kwargs)

        self.type = "TEXT"
        self.data = {
            "title": title
        }
        if code:
            self.data['code'] = code


class ButtonLink(Buttons):
    def __init__(self, title, url, mobile_url=None, **kwargs):
        super(ButtonLink, self).__init__(**kwargs)

        self.type = "LINK"
        self.data = {
            "title":title,
            "url":url,
            "mobile_url": mobile_url
        }


class ButtonOption(Buttons):
    def __init__(self, title, button_list, **kwargs):
        super(ButtonOption, self).__init__(**kwargs)

        if not isinstance(button_list, list):
            button_list = [button_list]
        self.type = "OPTION"
        self.data = {
            "title":title,
            "button_list": self.convert_shortcut_buttons(button_list)
        }


class ButtonPay(Buttons):
    def __init__(self, payment_info, **kwargs):
        super(ButtonPay, self).__init__(**kwargs)

        self.type = 'PAY'
        self.data = {
            'payment_info': payment_info
        }