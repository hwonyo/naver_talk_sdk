# naver_talk_sdk
[![PyPI](https://img.shields.io/pypi/v/nta.svg?v=1&maxAge=3601)](https://pypi.python.org/pypi/nta)
[![Coverage Status](https://coveralls.io/repos/github/HwangWonYo/naver_talk_sdk/badge.svg?branch=master)](https://coveralls.io/github/HwangWonYo/naver_talk_sdk?branch=master)
[![Build Status](https://travis-ci.org/HwangWonYo/naver_talk_sdk.svg?branch=master)](https://travis-ci.org/HwangWonYo/naver_talk_sdk)
[![PyPI](https://img.shields.io/pypi/l/nta.svg?v=1&maxAge=2592000?)](https://pypi.python.org/pypi/nta)

SDK of the NAVER TALK API for Python

# About the NAVERTALK Messaging API

#### Inspired By : [fbmq](https://github.com/conbus/fbmq) and [line-bot-sdk](https://github.com/line/line-bot-sdk-python>)

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
        "Echo Message:" % text
    )

```

## API
### NaverTalkApi
Create a new NaverTalk instance
```python
ntalk = nta.NaverTalkApi('YOUR_NAVER_TALK_ACCESS_TOKEN')
``` 

##### send(self, user_id, message, quick_replies=None, notification=False, callback=None)
send a message, to user with user_id
 


