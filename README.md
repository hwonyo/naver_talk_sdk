# naver_talk_sdk
[![PyPI](https://img.shields.io/pypi/v/nta.svg?v=1&maxAge=3601)](https://pypi.python.org/pypi/nta)
[![Coverage Status](https://coveralls.io/repos/github/HwangWonYo/naver_talk_sdk/badge.svg?branch=master)](https://coveralls.io/github/HwangWonYo/naver_talk_sdk?branch=master)
[![Build Status](https://travis-ci.org/HwangWonYo/naver_talk_sdk.svg?branch=master)](https://travis-ci.org/HwangWonYo/naver_talk_sdk)
[![PyPI](https://img.shields.io/pypi/l/nta.svg?v=1&maxAge=2592000?)](https://pypi.python.org/pypi/nta)

SDK of the NAVER TALK API for Python

# About the NAVERTALK Messaging API

__Inspired By : [fbmq](https://github.com/conbus/fbmq) and [line-bot-sdk](https://github.com/line/line-bot-sdk-python)__

## Install
```
pip install nta
```

## Synopsis
Usage (with flask)
```python
from flask import Flask, request
from nta import NaverTalkApi, NaverTalkApiError
from nta import Template


app = Flask(__name__)
ntalk = NaverTalkApi('your_naver_talk_access_token')


@app.route('/', methods=['POST'])
def message_handler():
    try:
        ntalk.webhook_handler(
            request.get_data(as_text=True)
        )
    except NaverTalkApiError as e:
        print(e)

    return "ok"
    

@ntalk.handle_open
def open_handler(event):
    """
    :param event: events.OpenEvent
    """
    user_id = event.user_id
    ntalk.send(
        user_id=user_id,
        message="Nice to meet you :)"
    )

@ntalk.handle_send
def send_handler(event):
    """
    :param event: events.SendEvent
    """
    user_id = event.user_id
    text = event.text
    ntalk.send(
        user_id,
        "Echo Message: %s" % text
    )

```

# API

* All attributes in Instances are same with snake case of the key name in json request from navertalk.
* See more info: [Naver Talk Github Page](https://github.com/navertalk/chatbot-api)

## NaverTalkApi
Create a new NaverTalk instance
```python
ntalk = nta.NaverTalkApi('YOUR_NAVER_TALK_ACCESS_TOKEN')
``` 

### handler

Handle event from user with decorators

The decorated Function gets [Event](##event) paramemter

##### __@handle_open__

- Open Event Handler
- [Open Event 정보](https://github.com/navertalk/chatbot-api#open-%EC%9D%B4%EB%B2%A4%ED%8A%B8)
```python
@ntalk.handle_open
def open_handler_function(event):
    user_id = event.user_id # str: 사용자 고유값
    inflow = event.inflow # str: 사용자 접근 방법
    refer = event.referer # str: 사용자 접근 url
    friend =  event.friend # bool: 사용자 친구 여부
    under_14 = event.under_14 # bool: 사용자 14세 미만 여부
    under_19 = event.under_19 # bool: 사용자 19세 미만 여부
```

##### __@handle_send__

- Send Event Handler
- [Send Event 정보](https://github.com/navertalk/chatbot-api#send-%EC%9D%B4%EB%B2%A4%ED%8A%B8)
```python
@ntalk.handle_send
def send_handler_function(event):
    user_id = event.user_id # str
    text = event.text # str: 사용자가 입력한 텍스트
    code = event.code # str: 사용자가 선택한 버튼의 값
    input_type = event.input_type # str: 사용자가 입력한 방식
    is_code = event.is_code # bool: code값 여부
    image_url = event.image_url # str: 사용자가 보낸 이미지 url

```
#### __@handle_leave__

- Leave Event Handler
- [Leave Event 정보](https://github.com/navertalk/chatbot-api#leave-%EC%9D%B4%EB%B2%A4%ED%8A%B8)
```python
@ntalk.handle_leave
def leave_handler_function(event):
    user_id = event.user_id
```

#### __@handle_friend__

- Friend Event Handler
- [Friend Event 정보](https://github.com/navertalk/chatbot-api#friend-%EC%9D%B4%EB%B2%A4%ED%8A%B8)
```python
@ntalk.handle_friend
def friend_handler_function(event):
    user_id = event.user_id
    set_on = event.set_on # bool: 친구추가 여부
```
#### __@handle_profile__

- Profile Event Handler
- [Profile Event 정보](https://github.com/navertalk/chatbot-api/blob/master/profile_api_v1.md)
```python
@ntalk.handle_profile
def profile_handler_function(event):
    user_id = event.user_id
    result = event.result # str: 사용자 동의 결과 SUCCESS|DISAGREE|CANCEL
    nickname = event.nickname # str: 사용자 이름 or None
    cellphone = event.cellphone # str: 사용자 연락처 or None
    address = event.address # str: 사용자 주소 or None
    
```

#### __@handle_pay_complete__

- PayComplete Event Handler
- [PayComplete Event 정보](https://github.com/navertalk/chatbot-api/blob/master/pay_api_v1.md#pay_complete-이벤트-구조)
```python
@handle_pay_complete
def pay_complete_handler(event):
    user_id = event.user_id
    code = event.code # str: 페이 성공 여부 Success|Fail
    payment_id event.payment_id # str 결제 성공시 결제번호
    merchant_pay_key = event.merchant_pay_key # str
    merchant_user_key = event.merchant_user_key # str
    message = event.message # str 결제 실패시 메세지
```
#### __@handle_pay_confirm__

- PayConfirm Event Handler
- [PayComfirm Event 정보](https://github.com/navertalk/chatbot-api/blob/master/pay_api_v1.md#pay_confirm-이벤트)
```python
@handle_pay_confirm
def pay_confirm_handler(event):
    user_id = event.user_id
    code = event.code # str
    message = event.message
    payment_id = event.payment_id
    detail = event.detail # 네이버페이 간편결제 승인 API 응답본문 detail 그대로 반환.
```
#### __@handle_echo__

- Echo Event Handler
- [Echo Event 정보](https://github.com/navertalk/chatbot-api#echo-%EC%9D%B4%EB%B2%A4%ED%8A%B8)
```python
@ntalk.handle_echo
def echo_handler_function(event):
    user_id = event.user_id
    pass
```

#### __@handle_before_process__

- Ahead of all event handler
- 이벤트 종류에 상관 없이 항상 실행
```python
@ntalk.handler_before_process
def before_process_function(event):
    user_id = event.user_id
```

#### __@after_send__

- Handler triggered after sending for each message to user
- ntalk.send를 성공할 때 마다 실행
- With two parameters [Response](###Response) and [Payload](###Payload) 
```python
@ntalk.after_send
def do_something_after_send_for_each_message(res, payload):
    # do something you want
    pass
```

#### __@callback__

- Callback Handler triggered when user clicks button with code value.
- After Callback Handling, [@handle_send](#####@handle_send) activated.
- Regular Expression can be used.
```python
@ntalk.callback
def calback_handler(event):
    user_id = event.user_id
    code = event.code
    
@ntalk.callback(['(^Hello).*'])
def hello_callback_handler(event):
    # This function will be triggered when a user hit the button contains code value starts with Hello
    code = event.code # ex) Hello Naver
```


__example__


#### Send a message
__send(self, user_id, message, quick_replies=None, notification=False, callback=None)__

- user_id *str*: 보내려는 유저의 고유 아이디
- message *Template* or *str*: 전송하고자 하는 메세지
- quick_replies *Template* or *list*: 빠른 답장
- notification *bool*: 푸쉬 메세지 설정 
- callback *func*: callback 함수. 메세지를 보내고 난 뒤에 실행된다.  

__Text__
```python
ntalk.send(user_id, "Hello Naver :)")
```
__Image__
```python
ntalk.send(user_id, Template.ImageContent(image_url))
```
or
```python
ntalk.send(user_id, Template.ImageContent(image_id=image_id))
```

__CompositeContent__
```python
ntalk.send(
    user_id,
    message=CompositeContent(composite_list=[ ... ])
)
```
__quick reply__
```python
quick_replies = QuickReply(
    [
        Button.TextButton('Punch', 'PunchCode'),
        Button.LinkButton('Link', 'https://example.link.com')
    ]
)
# can use a list of buttons instead of QuickReply instance
#
# quick_replies = [ {'title': 'Punch', 'value': 'PunchCode'},
#                    {'title': 'Link', 'value': 'https://example.link.com'}]

ntalk.send(
    user_id,
    "Quick Reply message",
    quick_replies=quick_replies
)
```



 


