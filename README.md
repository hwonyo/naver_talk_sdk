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

* All attributes in Instances is same with snake case of the key name in json request from navertalk.
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

##### __@handle_send__

- Send Event Handler
```python
@ntalk.handle_send
def send_handler_function(event):
    user_id = event.user_id
    text = event.text

```
#### __@handle_leave__

- Leave Event Handler

#### __@handle_friend__

- Friend Event Handler

#### __@handle_profile__

- Profile Event Handler

#### __@handle_pay_complete__

- PayComplete Event Handler

#### __@handle_pay_confirm__

- PayConfirm Event Handler

#### __@handle_echo__

- Echo Event Handler

#### __@handle_before_process__

- Ahead of all event handler

#### __@after_send__

- Handler triggered after sending for each message to user
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

__Text__
```python
ntalk.send(user_id, "Hello Naver :)")
```
__Image__
```python
ntalk.send(user_id, Template.ImageContent(image_url))
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



 


