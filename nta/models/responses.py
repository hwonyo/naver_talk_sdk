from .base import Base

class Response(Base):
    pass


class NaverTalkResponse(Response):
    """NaverTalkResponse
    For Parsing response from navertalk after sending a message request."""
    def __init__(self, success, result_code, result_message=None, **kwargs):
        """__init__ method.

        Args:
            -success: True or False
            -result_code: str result code can see more info in navertalk github page.
            -result_message: str result message when request failed.
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

        Args:
            -success: True or False
            -result_code: str result code can see more info in navertalk github page.
            -image_id: str image_id when request success.
            -result_message: str result message when request failed.
        """
        super(NaverTalkImageResponse, self).__init__(**kwargs)

        self.success = success
        self.result_code = result_code
        self.image_id = image_id
        self.result_message = result_message