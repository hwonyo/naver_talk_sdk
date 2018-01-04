#-*- encoding:utf-8 -*-
import os
from flask import Flask, request
from nta import NaverTalkApi, Template, NaverTalkApiError, Button, NaverTalkPaymentError, NaverTalkApiConnectionError


NAVER_TALK_ACCESS_TOKEN = os.environ['naver_talk_access_token']

app = Flask(__name__)
ntalk = NaverTalkApi(NAVER_TALK_ACCESS_TOKEN)


@app.route('/', methods=['POST'])
def app_enterance():
    print("*" * 40)
    req = request.get_data(as_text=True)
    print('* Recieved Data:')
    print(req)
    try:
        ntalk.webhook_handler(req)
    except NaverTalkApiError as e:
        print(e)
    except NaverTalkApiConnectionError as e:
        print(e)
    except NaverTalkPaymentError as e:
        return 400

    print("*" * 40)

    return "ok"


@ntalk.before_proccess
def do_something_before_event_handle(event):
    print('#' * 40)
    print('* EventType: %10s' % event.__class__.__name__)
    print('* User Id  : %10s '% event.user_id)

@ntalk.handle_open
def open_handler(event):
    user_id = event.user_id
    ntalk.send(
        user_id,
        "테스트에 성공했구나 :)"
    )

@ntalk.handle_send
def send_handler(event):
    """
    사용자가 버튼을 눌러 코드값 callback을 사용해도 send_handler가 작동한다.
    만약 코드 값의 callback 함수만 동작하게 하고 싶다면 is_code일 경우 return 하면된다.
    """
    if event.is_code:
        return

    user_id = event.user_id
    if event.standby:
        ntalk.send(
            user_id=user_id,
            message="쓰레드 작동중 !!",
            quick_reply=Template.QuickReply([Button.ButtonText('쓰레드 가져오기', 'TakeThread')])
        )
        return
    text = event.text
    ntalk.send(user_id, "당신이 한 말을 그대로 반환 나는 메아리: %s" % text)
    ntalk.send(
        user_id,
        message=Template.CompositeContent(
            composite_list=[
                Template.Composite(
                    title='페이로드 백을 담은 카드뷰',
                    description='상세 설명',
                    button_list=[
                        {'type': 'TEXT', 'title': '쓰레드 넘김', 'value': 'PassThread'},
                        Button.ButtonText('타이핑 액션', 'TYPING_ON')
                    ]
                ),
                Template.Composite(
                    title='링크 버튼을 담은 카드뷰',
                    description='이건 회색 글씨로 나온다!',
                    button_list=[
                        {'type': 'LINK', 'title': 'nta github page', 'value': 'https://github.com/HwangWonYo/naver_talk_sdk'},
                        Button.ButtonLink('네이버 파트너 센터', 'https://partner.talk.naver.com/')
                    ]
                )
            ]
        )
    )


@ntalk.callback(['TYPING_ON'])
def action_typing(event):
    print("Activate typing_on")
    user_id = event.user_id
    ntalk.typing_on(user_id)


@ntalk.callback(['PassThread'])
def thread_pass(event):
    print('pass thread')
    user_id = event.user_id
    ntalk.pass_thread(
        user_id=user_id,
        partner="wc4qdz"
    )
    ntalk.send(user_id, "쓰레드 넘기기 성공")


@ntalk.callback(['TakeThread'])
def thread_take(event):
    print('take thread')
    user_id = event.user_id
    ntalk.take_thread(
        user_id=user_id,
        partner="wc4qdz"
    )
    ntalk.send(user_id, "쓰레드 반환 받기 성공")


@ntalk.after_send
def do_something_after_send(res, payload):
    print('* Message Type: %s' % payload.__class__.__name__)


if __name__ == "__main__":
    app.run()