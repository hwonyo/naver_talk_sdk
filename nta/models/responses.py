from .base import Base

class Response(Base):
    pass


class NaverTalkResponse(Response):

    def __init__(self, success, result_code, result_message=None, **kwargs):
        super(NaverTalkResponse, self).__init__(**kwargs)

        self.success = success
        self.result_code = result_code
        self.result_message = result_message


class NaverTalkImageResponse(Response):

    def __init__(self, success, result_code, image_id=None, result_message=None, **kwargs):
        super(NaverTalkImageResponse, self).__init__(**kwargs)

        self.success = success
        self.result_code = result_code
        self.image_id = image_id
        self.result_message = result_message