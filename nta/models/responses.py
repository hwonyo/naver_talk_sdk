from .base import Base

class Response(Base):
    pass


class NaverTalkResponse(Response):
    """NaverTalkResponse
    For Parsing response from navertalk after sending a message request."""
    def __init__(self, success, result_code, result_message=None, **kwargs):
        """__init__ method.

        :param success: True or False
        :param result_code: str result code can see more info in navertalk github page.
        :param result_message: str result message when request failed.
        :param kwargs:
        """
        super(NaverTalkResponse, self).__init__(**kwargs)

        self.success = success
        self.result_code = result_code
        self.result_message = result_message


class NaverTalkImageResponse(Response):
    """NaverTalkImageResponse
    For Parsing response from navertalk after sending an image upload request"""
    def __init__(self, success, result_code, image_id=None, result_message=None, **kwargs):
        """ __init__ method.

        :param success: True or False
        :param result_code: str result code can see more info in navertalk github page.
        :param image_id: str image_id when request success.
        :param result_message: str result message when request failed.
        :param kwargs:
        """
        super(NaverTalkImageResponse, self).__init__(**kwargs)

        self.success = success
        self.result_code = result_code
        self.image_id = image_id
        self.result_message = result_message