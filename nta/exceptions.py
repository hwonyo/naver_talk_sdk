'''navertalk.exceptions module.'''
from __future__ import unicode_literals
from .utils import LOGGER

class BaseError(Exception):
    """Base Exception class"""

    def __init__(self, message='-'):
        """__init__ method.

        :param str message: Readable message
        """
        self.message = message

    def __repr__(self):
        """repr.

        :return:
        """
        return str(self)

    def __str__(self):
        """str.

        :rtype: str
        :return:
        """
        return '<%s [%s]>' % (self.__class__.__name__, self.message)


class NaverTalkApiError(BaseError):
    """When Naver Talk failed to build message, this error will be raised"""

    def __init__(self, api_response):
        """__init__ method.

        :param response error_api_response: Response class object
        """
        super(NaverTalkApiError, self).__init__(api_response.result_message)

        self._status_code = 200
        self.result_code = api_response.result_code

    @property
    def status_code(self):
        """

        status_code always return 200
        :rtype int:
        :return:
        """

        return self._status_code


class NaverTalkApiConnectionError(BaseError):
    """When Naver Talk Api response error, this error will be raised"""

    def __init__(self, response):
        """___init__ method.

        :param response response: request.response
        """
        super(NaverTalkApiConnectionError, self).__init__(response.text)

        self.status_code = response.status_code
        self.response = response

class NaverTalkPaymentError(BaseError):
    pass