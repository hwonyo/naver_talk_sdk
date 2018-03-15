# naver_talk_sdk
[![PyPI](https://img.shields.io/pypi/v/nta.svg?v=1&maxAge=3601)](https://pypi.python.org/pypi/nta)
[![Coverage Status](https://coveralls.io/repos/github/HwangWonYo/naver_talk_sdk/badge.svg?branch=master)](https://coveralls.io/github/HwangWonYo/naver_talk_sdk?branch=master)
[![Build Status](https://travis-ci.org/HwangWonYo/naver_talk_sdk.svg?branch=master)](https://travis-ci.org/HwangWonYo/naver_talk_sdk)
[![PyPI](https://img.shields.io/pypi/l/nta.svg?v=1&maxAge=2592000?)](https://pypi.python.org/pypi/nta)

SDK of NAVER TALK API for Python
__Inspired By : [fbmq](https://github.com/conbus/fbmq) and [line-bot-sdk](https://github.com/line/line-bot-sdk-python)__

> 네이버 톡톡 파이썬 모듈입니다.<br>
> 톡톡에서 발생하는 "__이벤트를 중심__"으로 효율적인 코드를 짤 수 있습니다. <br>
> [callback handler](#callback)를 이용하면 버튼의 payload 값에 따라 처리를 분기할 수 있습니다.


# About NAVERTALK Messaging API
## Table of Contents

* [Install](#install)
* [Synopsis](#synopsis)
* [API](#api)
  - [NaverTalkApi](#navertalkapi)
    - [handler](#handler)
      - [@handle_open](#handle_open)
      - [@handle_send](#handle_send)
      - [@handle_leave](#handle_leave)
      - [@handle_friend](#handle_friend)
      - [@handle_profile](#handle_profile)
      - [@handle_pay_complete](#handle_pay_complete)
      - [@handle_pay_confirm](#handle_pay_confirm)
      - [@handle_echo](#handle_echo)
      - [@handle_handover](#handle_handover)
      - [@handle_before_process](#handle_before_process)
      - [@after_send](#after_send)
      - [@callback](#callback)
    - [Send message](#send-message)
      - [Text](#text)
      - [Image](#image)
      - [CompositeContent](#compositecontent)
      - [quick reply](#quick-reply)
    - [Utility](#utility)
      - [take_thread](#take_threadself-user_id-callbacknone)
      - [pass_thread](#pass_threadself-user_id-callbacknone)
      - [typing_on](#typing_onself-user_id-callbacknone)
      - [typing_off](#typing_offself-user_id-callbacknone)
      - [persistent_menu](#persistent_menuself-menus-callbacknone)
  - [Template](#template)
    - [TextContent](#textcontent)
    - [ImageContent](#imagecontent)
    - [CompositeContent](#compositecontent)
    - [Composite](#composite)
    - [ElementList](#elementlist)
    - [ElementData](#elementdata)
    - [QuickReply](#quickreply)
    - [PaymentInfo](#paymentinfo)
    - [ProductItem](#productitem)
  - [Buttons](#buttons)
    - [ButtonText](#buttontext)
    - [ButtonLink](#buttonlink)
    - [ButtonOption](#buttonoption)
    - [ButtonTime](#buttontime)
    - [ButtonNested](#buttonnested)
    - [ButtonCalendar](#buttoncalendar)
  - [Exception](#exception)
    - [NaverTalkApiError](#navertalkapierror)
    - [NaverTalkApiConnectionError](#navertalkapiconnectionerror)
    - [NaverTalkPaymentError](#navertalkpaymenterror)
  - [Event](#event)
    - [OpenEvent](#openevent)
    - [LeaveEvent](#leaveevent)
    - [FriendEvent](#friendevent)
    - [SendEvent](#sendevent)
    - [EchoEvent](#echoevent)
    - [PayCompleteEvent](#paycompleteevent)
    - [PayConfirmEvent](#payconfirmevent)
    - [HandOverEvent](#handoverevent)
     
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
See more detail example code: [example/example.py](https://github.com/HwangWonYo/naver_talk_sdk/blob/master/example/example.py)

And see also implemented naver talktalk agent: https://talk.naver.com/ct/wc4qdz 

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

Decorated Function takes [Event](#event) paramemter

#### __@handle_open__

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
    mobile = event.mobile # bool: 모바일 사용 여부
    standby = event.standby # bool: 상담사와 연결된 경우 True
```

#### __@handle_send__

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
    mobile = event.mobile # bool: 모바일 사용 여부
    standby = event.standby # bool: 상담사와 연결된 경우 True
```
#### __@handle_leave__

- Leave Event Handler
- [Leave Event 정보](https://github.com/navertalk/chatbot-api#leave-%EC%9D%B4%EB%B2%A4%ED%8A%B8)
```python
@ntalk.handle_leave
def leave_handler_function(event):
    user_id = event.user_id
    mobile = event.mobile # bool: 모바일 사용 여부
    standby = event.standby # bool: 상담사와 연결된 경우 True
```

#### __@handle_friend__

- Friend Event Handler
- [Friend Event 정보](https://github.com/navertalk/chatbot-api#friend-%EC%9D%B4%EB%B2%A4%ED%8A%B8)
```python
@ntalk.handle_friend
def friend_handler_function(event):
    user_id = event.user_id
    set_on = event.set_on # bool: 친구추가 여부
    mobile = event.mobile # bool: 모바일 사용 여부
    standby = event.standby # bool: 상담사와 연결된 경우 True
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
    mobile = event.mobile # bool: 모바일 사용 여부
    standby = event.standby # bool: 상담사와 연결된 경우 True
```

#### __@handle_pay_complete__

- PayComplete Event Handler
- [PayComplete Event 정보](https://github.com/navertalk/chatbot-api/blob/master/pay_api_v1.md#pay_complete-이벤트-구조)
```python
@ntalk.handle_pay_complete
def pay_complete_handler(event):
    user_id = event.user_id
    code = event.code # str: 페이 성공 여부 Success|Fail
    payment_id = event.payment_id # str 결제 성공시 결제번호
    merchant_pay_key = event.merchant_pay_key # str
    merchant_user_key = event.merchant_user_key # str
    message = event.message # str 결제 실패시 메세지
    mobile = event.mobile # bool: 모바일 사용 여부
    standby = event.standby # bool: 상담사와 연결된 경우 True
```
#### __@handle_pay_confirm__

- PayConfirm Event Handler
- [PayComfirm Event 정보](https://github.com/navertalk/chatbot-api/blob/master/pay_api_v1.md#pay_confirm-이벤트)
```python
@ntalk.handle_pay_confirm
def pay_confirm_handler(event):
    user_id = event.user_id
    code = event.code # str
    message = event.message
    payment_id = event.payment_id
    detail = event.detail # 네이버페이 간편결제 승인 API 응답본문 detail 그대로 반환.
    mobile = event.mobile # bool: 모바일 사용 여부
    standby = event.standby # bool: 상담사와 연결된 경우 True
```
#### __@handle_echo__

- Echo Event Handler
- [Echo Event 정보](https://github.com/navertalk/chatbot-api#echo-%EC%9D%B4%EB%B2%A4%ED%8A%B8)
```python
@ntalk.handle_echo
def echo_handler_function(event):
    user_id = event.user_id
    mobile = event.mobile # bool: 모바일 사용 여부
    standby = event.standby # bool: 상담사와 연결된 경우 True
    text_content = event.text_content # dict: text_content or None
    image_content = event.image_content # dict: image_content or None
    composite_content = event.composite_content # dict: composite_content or None
    pass
```
#### __@handle_handover__

- Handover Event Handler
- [Handover Event 정보](https://github.com/navertalk/chatbot-api/blob/master/handover_v1.md)
```python
@ntalk.handle_handover
def handover_handler_function(event):
    user_id = event.user_id
    control = event.control # 주도권이 챗봇에게 넘어온 경우 (발생하는 이벤트의 컨트롤은 항상 passThread)
    metadata = event.metadata # 넘어오는 메타 데이터.
```


#### __@handle_before_process__

- Ahead of all event handler
- 이벤트 handler를 사용하기 전에 실행되는 함수. (event 종류에 상관없이 실행된다.)
```python
@ntalk.handler_before_process
def before_process_function(event):
    user_id = event.user_id
    pass
```

#### __@after_send__

- Handler triggered after sending for each message to user
- ntalk.send를 성공할 때 마다 실행
- With two parameters [Response](#response) and [Payload](#payload) 
```python
@ntalk.after_send
def do_something_after_send_for_each_message(res, payload):
    # do something you want
    pass
```

#### __@callback__

- Callback Handler triggered when user clicks button with code value.
- After Callback Handling, [@handle_send](#handle_send) is activated.
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

## Send message
### __send(self, user_id, message, quick_reply=None, notification=False, callback=None)__

- user_id *str*: 보내려는 유저의 고유 아이디
- message *Template* or *str*: 전송하고자 하는 메세지
- quick_reply *Template* or *list*: 빠른 답장
- notification *bool*: 푸쉬 메세지 설정 
- callback *func*: callback 함수. 메세지를 보내고 난 뒤에 실행된다.  

#### __Text__

```python
ntalk.send(user_id, "Hello Naver :)")
```
or
    
```python
ntalk.send(user_id, Template.TextContent("Hello Naver :)")
```
    
#### __Image__
```python
ntalk.send(user_id, Template.ImageContent(image_url))
```
or

```python
ntalk.send(user_id, Template.ImageContent(image_id=image_id))
```

#### __CompositeContent__
```python
ntalk.send(
    user_id,
    message=CompositeContent(composite_list=[ ... ])
)
```
#### __quick reply__
```python
quick_reply = QuickReply(
    [
        Button.TextButton('Punch', 'PunchCode'),
        Button.LinkButton('Link', 'https://example.link.com')
    ]
)
# can use a list of buttons instead of QuickReply instance
#
# quick_reply = [ {'title': 'Punch', 'value': 'PunchedCode'},
#                    {'title': 'Link', 'value': 'https://example.link.com'}]

ntalk.send(
    user_id,
    "Quick Reply message",
    quick_reply=quick_reply
)
```

## Utility
### __take_thread(self, user_id, callback=None)__

- user_id: 권한을 넘길 사용자
- callback: callback 함수
- [자세한 정보](https://github.com/navertalk/chatbot-api/blob/master/handover_v1.md#%EC%B1%97%EB%B4%87%EC%9D%B4-%EB%8C%80%ED%99%94%EC%9D%98-%EC%A3%BC%EB%8F%84%EA%B6%8C%EC%9D%84-%EA%B0%80%EC%A0%B8%EC%98%A4%EA%B8%B0)
```python
ntalk.take_thread(
    user_id=user_id
    )
```

### __pass_thread(self, user_id, callback=None)__

- user_id: 권한을 넘길 사용자
- callback: callback 함수
- [자세한 정보](https://github.com/navertalk/chatbot-api/blob/master/handover_v1.md#%EC%B1%97%EB%B4%87%EC%9D%98-%EB%A9%94%EC%8B%9C%EC%A7%80%EB%A5%BC-%EC%88%98%EC%8B%A0%ED%95%A0-%EB%95%8C-standby-%EC%86%8D%EC%84%B1)
```python
ntalk.pass_thread(
    user_id=user_id,
)
```

### __typing_on(self, user_id, callback=None)__

- user_id:
- callback: callback 함수
- [자세한 정보](https://github.com/navertalk/chatbot-api#action-%EC%9D%B4%EB%B2%A4%ED%8A%B8)
```python
ntalk.typing_on(user_id)
``` 

### __typing_off(self, user_id, callback=None)__

- user_id: 사용자 아이디
- callback: callback 함수
- [자세한 정보](https://github.com/navertalk/chatbot-api#action-%EC%9D%B4%EB%B2%A4%ED%8A%B8)
```python
ntalk.typing_off(user_id)
```

### __persistent_menu(self, menus, callback=None)__

- menus: `<type list>`  고정메뉴에 보여질 버튼 ( ButtonOption is not allowed )
- [자세한 정보](https://github.com/navertalk/chatbot-api#persistentmenu-%EC%9D%B4%EB%B2%A4%ED%8A%B8)
```python
ntalk.persistent_menu(menus=[Button.ButtonText(...), Button.ButtonLink(...), ...])
```

## Template

```python
from nta import Template
```

### TextContent
> __init__(self, text, code=None, input_type=None, **kwargs)

- text: 사용자에게 보낼 텍스트
- code: 사용자에게 받은 텍스트
- input_type: 사용자 입력 타입
- [textContent 정보](https://github.com/navertalk/chatbot-api#textcontent)
```python
Template.TextContent('너에게 보내는 메세지')
```

### ImageContent
> __init__(self, image_url=None, image_id=None, **kwargs)

- image_url: 사용자에게 보낼 이미지 url
- image_id: 사용자에게 보낼 이미지 id
- image_url과 image_id 중 하나를 반드시 포함 (image_url 우선)
- [imageContent 정보](https://github.com/navertalk/chatbot-api#imagecontent)
    ```python
    Template.ImageContent(image_url='xxx.jpg')
    ```
### CompositeContent 
> __init__(self, composite_list, **kwargs)

- 카드뷰 형식의 탬플릿
- composite_list: [composite](#composite) 리스트 
- [compositeContent 정보](https://github.com/navertalk/chatbot-api#compositecontent)
```python
Template.CompositeContent(
    composite_list = [Template.Composite(...), ...]
)
```


### Composite
> __init__(self, title, description=None, image=None, element_list=None, button_list=None, **kwargs)

- title: 카드의 타이틀
- description: 카드의 상세설명
- image: 카드에 보이는 이미지 url or 이미지 id
- element_list: 카드를 구성하는 [ElementData](#elementdata) 리스트
- button_list: 카드를 구성하는 [Button](#buttons) 리스트
- [composite 정보](https://github.com/navertalk/chatbot-api#composite-object)

```python
Template.Composite(
    title="굵은글씨",
    description="회색글씨",
    image="xxx.jpg",
    element_list=Template.ElementList([
        Template.ElementData(...), 
        ...
    ]),
    button_list=[
        Template.ButtonText(...),
        ...
    ]
)
```

### ElementList
> __init__(self, data, **kwargs)

- data: [ElementData](#elementdata) 리스트
- [ElementList 정보](https://github.com/navertalk/chatbot-api#elementlist-object)
```python
Template.ElementList(data=[
    Template.ElementData(...),
    ...
])
```

### ElementData
> __init__(self, title, description=None, sub_description=None, image=None, button=None, **kwargs)

- title: Element 타이틀
- description: 상세정보
- sub_dscription: 하위 상세정보
- image: 이미지 url or 이미지 id
- button: Template.Button 버튼 하나
- [ElementData 정보](https://github.com/navertalk/chatbot-api#elementdata-object-list-%ED%83%80%EC%9E%85)
```python
Template.ElementData(
    title="굵은글씨",
    description="회색글씨",
    sub_description="더 회색글씨",
    image="xxx.jpg",
    button=Template.ButtonText(...)
)
```

### QuickReply
> __init__(self, button_list, **kwargs)

- button_list: 버튼 리스트
- [quickReply 정보](https://github.com/navertalk/chatbot-api#%ED%80%B5%EB%B2%84%ED%8A%BC)
```python
Template.QuickReply([
    Template.ButtonText(...),
    ...
])
```

### PaymentInfo
> __init__(self, merchant_pay_key, total_pay_amount, product_items, merchant_user_key=None, ...)

- merchant_pay_key: 필수
- total_pay_amount: 필수 
- product_items: 필수 [ProductItem](#productitem) 리스트
- 자세한 정보 및 나머지 값들 [PaymentInfo](https://github.com/navertalk/chatbot-api/blob/master/pay_api_v1.md#paymentinfo-오브젝트) 참고
```python
Template.ProductInfo(
    merchant_pay_key="yo-product-123",
    total_pay_amount=100000000,
    product_items=[
        Template.ProductItem(...),
        ...
    ],
    ...
)
```

### ProductItem
> __init__(self, category_type, category_id, uid, name, ...)

- category_type: 필수
- category_id: 필수
- uid: 필수
- name: 필수
- 자세한 정보 및 나머지 값들 [productItem](https://github.com/navertalk/chatbot-api/blob/master/pay_api_v1.md#productitem-오브젝트)참고
```python
Template.ProductItem(
    category_type="Book",
    category_id="yo-123-book",
    uid="7269889",
    name="yosbest",
    ...
```
## Buttons
```python
from nta import Button
```
### ButtonText
> __init__(self, title, code=None, **kwargs)

- title: 버튼 값.
- code : 버튼에 숨겨진 code 값.
- 자세한 정보 [buttonText](https://github.com/navertalk/chatbot-api#buttondata-object-text-타입)
```python
Button.ButtonText('보여지는 타이틀', '숨겨진 코드값')
```

### ButtonLink
> __init__(self, title, url, mobile_url=None, webview=True, webview_title=None, webview_height=None, **kwargs)

- title: 보여지는 버튼 값.
- url : 연결되는 링크
- mobile_url: 모바일 상에서 연결되는 링크.
- webview: True or False. If True, activate webview button
- webview_title: title of webview
- webview_height: size ratio of webview
- 자세한 정보 [buttonLink](https://github.com/navertalk/chatbot-api#buttondata-object-link-타입)
- webview에 대한 정보 [webview](https://github.com/navertalk/chatbot-api/blob/master/webview_v1.md)
```python
Button.ButtonLink(
        "title showed up", 
        "Linked URL", 
        mobile_url="#Linked URL in Mobile device",
        webview=True,
        webview_title="Title of webview",
        webview_height=50
    )
```

### ButtonOption
> __init__(self, title, button_list, **kwargs)

- title: 노출되는 텍스트
- button_list: 숨겨진 버튼
- 자세한 정보 [buttonOption](https://github.com/navertalk/chatbot-api#buttondata-object-option-타입)
```python
Button.ButtonOption("title showed up", button_list=[Button.ButtonText(...), ...])
```

### ButtonTime
> __init__(self, title, code, **kwargs)

- title: 노출되는 텍스트
- code: 버튼의 코드값
- 자세한 정보 [ButtonTime](https://github.com/navertalk/chatbot-api/blob/master/time_component_v1.md)
```python
Button.ButtonTime("title showed up", code='Time_Test')

# Use callback regex matching makes it easy to use
# example callback handler below.
ntalk.callback(['Time_Test'])
def time_test_handler(event):
    # event.title: user selected time
    pass
```

### ButtonNested
> __init__(self, title, menus, **kwargs)

- 고정 메뉴에 사용되는 버튼이다. 버튼을 누르면 숨겨진 버튼이 보여진다.
- title: 노출되는 텍스트
- menus: `<type list>` 버튼 리스트
- 자세한 정보 [ButtonNested](https://github.com/navertalk/chatbot-api#menudata-objectnested-%ED%83%80%EC%9E%85)
```python
Button.ButtonNested("title showed up", menus=[Button.ButtonText(...), Button.ButtonLink(...), ...]
```

### ButtonCalendar
> __init__(self, title=None, code=None, placeholder=None, start=None, end=None, disables=None, **kwargs)

- Use built-in calendar webview provided by Naver.
- title: Exposed to button.
- code: Hidden code in button.
- palceholder: Webview title.
- start: start date.
- end: end date.
- disalbes: date to disable.
- More Info See [ButtonCalnedar](https://github.com/navertalk/chatbot-api/blob/master/calendar_component_v1.md)
```python
Button.ButtonCalnedar(title="title showed up", code="hidden code", ...)
```

## Exception
```python
from nta.exceptions import (
    NaverTalkApiError,
    NaverTalkPaymentError,  
    NaverTalkApiConnectionError
    )

def webhook_handler():
    req = requests.get_data(as_text=True)
    try:
        ntalk.handle_webhook(req)
    except NaverTalkApiError as e:
        assert e.status_code == 200
        assert e.result_code != "00"
        # e.message from navertalk
    except NaverTalkApiConnectionError as e:
        assert e.status_code != 200
    except NaverTalkPaymentError as e:
        return e.message, 400
    
    return "ok"
    
```
### NaverTalkApiError

- Naver Talk에 Post 이후 받은 값 Success가 False인 경우 발생
- resultCode가 "00"이 아닌 경우 발생.
- 더 많은 result코드와 내용에 대한 정보 [Error](https://github.com/navertalk/chatbot-api#error-명세서)

### NaverTalkApiConnectionError

- NaverTalk api internal server error.
- 네이버톡으로 부터 200이 아닌 response를 받았을 때 발생.

### NaverTalkPaymentError

- 결제를 취소를 위한 error
- 사용자의 결제를 승인을 거부할 때 사용.
- Pay 개발가이드 참고 [Pay](https://github.com/navertalk/chatbot-api/blob/master/pay_api_v1.md#개발가이드)

example
```python
@ntalk.handle_pay_complete
def pay_handle_func(event):
    if not 재고:
        raise NaverTalkPaymentError('재고 없음') 
```

## Event
<span style="color:gray">handler만 참고 하면 사용에 어려움 없음. 심리적 안정을 위해 추가한 섹션.</span>
- 이벤트의 사용은 [handler](#handler) 참고
- Event.user_id: 사용자 아이디. (모든 이벤트에 해당함.)
### OpenEvent
- OpenEvent.inflow: 사용자 유입방식
- OpenEvent.referer: 사용자 유입경로
- OpenEvent.friend: 사용자가 친구일 경우 True
- OpenEvent.under_14: 사용자가 14세 미만일 경우 True
- OpenEvent.under_19: 사용자가 19세 미만일 경우 True
- [OpenEvent 참고](https://github.com/navertalk/chatbot-api#open-%EC%9D%B4%EB%B2%A4%ED%8A%B8)

### LeaveEvent

- [LeaveEvent 참고](https://github.com/navertalk/chatbot-api#leave-이벤트)

### FriendEvent
- FriendEvent.set_on: 사용자가 친구 추가할 경우 True
- [FriendEvent 참고](https://github.com/navertalk/chatbot-api#friend-이벤트)


### SendEvent

- SendEvent.text: 사용자가 입력한 문장
- SendEvent.code: 사용자가 선택한 버튼의 code값
- SendEvent.input_type: 사용자가 입력을 한 방식.
- SendEvent.is_code: 사용자의 입력에 코드값이 포함되어 있을 경우.
- SendEvent.image_url: 사용자가 보낸 이미지의 url
- [SendEvent 참고](https://github.com/navertalk/chatbot-api#send-이벤트)

### EchoEvent
 
- EchoEvent.echoed_event: echo 이벤트에 담겨있는 모든 정보
- [EchoEvent 참고](https://github.com/navertalk/chatbot-api#echo-이벤트)

### PayCompleteEvent

- PayCompleteEvent.payment_result: 사용자 결제 결과.
- PayCompleteEvent.code: 사용자 결제 결과 코드.
- PayCompleteEvent.payment_id: 결제 식별 고유번호. (결제 성공시)
- PayCompleteEvent.message: 결제 실패 정보. (결제 실패시)
- PayCompleteEvent.merchant_pay_key: custum 결제 식별 정보.
- PayCompleteEvent.merchant_user_key: custum 유저 식별 정보.
- [PayCompleteEvent 참고](https://github.com/navertalk/chatbot-api/blob/master/pay_api_v1.md#pay_complete-이벤트-구조)

### PayConfirmEvent

- PayConfirmEvent.code: 결제승인 결과
- PayConfirmEvent.message: 결제승인 결과 메세지
- PayConfirmEvent.payment_id: 결제 식별 고유번호 (결제 성공시 ?)
- PayConfirmEvent.detail: d네이버페이 간편결제 결제승인 API 응답본문 그대로 반환.
- [PayConfirmEvent 참고](https://github.com/navertalk/chatbot-api/blob/master/pay_api_v1.md#pay_confirm-이벤트)

### HandOverEvent

- HandOverEvent.control: passThread
- HandOverEvent.metadata: 네이버톡톡에서 보내온 메타 데이터