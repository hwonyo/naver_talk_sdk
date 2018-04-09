#-*- encoding:utf-8 -*-
"""
    Example code for nta
    See how it works: https://talk.naver.com/ct/wc4qdz
"""
import os
from flask import Flask, request

from nta import NaverTalkApi, Template, Button
from nta import NaverTalkApiError, NaverTalkPaymentError, NaverTalkApiConnectionError

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
        "테스트에 성공했구나 :)",
        quick_reply=Template.QuickReply([
            Button.ButtonLink(
                "코드 보러가기",
                "https://github.com/HwangWonYo/naver_talk_sdk/blob/master/example/example.py"
            ),
            Button.ButtonText(
                "따라 말하기"
            )
        ])
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
    text = event.text

    #주도권이 파트너에게 있는 경우 standby는 True
    if event.standby:
        ntalk.send(
            user_id=user_id,
            message="쓰레드 작동중 !!",
            quick_reply=Template.QuickReply([Button.ButtonText('쓰레드 가져오기', 'TakeThread')])
        )
    else:
        ntalk.send(
            user_id,
            "무슨 말을 해도 따라합니다.\n"
            "카드뷰 형식을 보고 싶으면 퀵리플라이 클릭"
        )
        ntalk.send(
            user_id,
            text,
            quick_reply=Template.QuickReply([Button.ButtonText('카드뷰 보기', 'CardView')])
        )


@ntalk.callback(['CardView'])
def carview_show(event):
    user_id = event.user_id
    ntalk.send(
        user_id,
        message=Template.CompositeContent(
            composite_list=[
                Template.Composite(
                    title='페이로드 백을 담은 카드뷰',
                    description='상세 설명',
                    button_list=[
                        Button.ButtonText('쓰레드 넘김', 'PassThread'),
                        Button.ButtonText('타이핑 액션', 'TYPING_ON'),
                        Button.ButtonText('프로필 보기', 'Profile')
                    ]
                ),
                Template.Composite(
                    title='링크 버튼을 담은 카드뷰',
                    description='이건 회색 글씨로 나온다!',
                    button_list=[
                        Button.ButtonLink('nta github page', 'https://github.com/HwangWonYo/naver_talk_sdk'),
                        Button.ButtonLink('네이버 파트너 센터', 'https://partner.talk.naver.com/'),
                        Button.ButtonText('ElementList 카드뷰', 'ElementListCardView')
                    ]
                ),
                Template.Composite(
                    title='세번째 카드 리스트',
                    description='1. Time Component',
                    button_list=[
                        Button.ButtonTime('시간을 눌러봅시다.', code='Time_Test'),
                        Button.ButtonCalendar(
                            '날짜를 선택해봅시다.',
                            code='Calendar_Test',
                            placeholder='글자 수 제한이 있을까? 이 친구는 5월만 고를 수 있어. 또 일요일은 빼자',
                            start='20180501',
                            end='20180531',
                            disables='0'
                        ),
                        Button.ButtonTimeInterval(
                            '시간을 선택해봅시다.',
                            code='TimeInterval_test'
                        )
                    ]
                ),
                Template.Composite(
                    title='네번째 카드 리스트',
                    description='New Payload !',
                    button_list=[
                        Button.ButtonText('Product Message 보기', 'SHOW_PRODUCT_MESSAGE')
                    ]
                )
            ]
        )
    )


@ntalk.callback(['SHOW_PRODUCT_MESSAGE'])
def product_message_handler(event):
    user_id = event.user_id
    ntalk.product_message(
        user_id,
        ids=[
            12345,
            12344,
            12343
        ],
        display_type='list'
    )


@ntalk.callback(['TimeInterval_test'])
def time_interval_handler(event):
    user_id = event.user_id
    text = event.text
    ntalk.send(
        user_id,
        '선택하신 시간은 {} 입니다.'.format(text),
        quick_reply=Template.QuickReply(
            [Button.ButtonText('카드뷰 보기', 'CardView')]
        )
    )


@ntalk.callback(['Time_Test'])
def time_component_handler(event):
    user_id = event.user_id
    text = event.text
    ntalk.send(
        user_id,
        '선택하신 시간은 {} 이군요'.format(text),
        quick_reply=Template.QuickReply(
            [Button.ButtonText('카드뷰 보기', 'CardView')]
        )
    )


@ntalk.callback(['Calendar_Test'])
def calendar_handler(event):
    user_id = event.user_id
    text = event.text
    ntalk.send(
        user_id,
        '선택하신 날짜는 {} 이군요.'.format(text),
        quick_reply=Template.QuickReply(
            [
                Button.ButtonText('카드뷰 보기', 'CardView'),
                Button.ButtonCalendar(
                    title='날짜 다시 선택하기',
                    code='Calendar_Test',
                    placeholder='다시 선택 하는 거다',
                    start='20180305',
                    end='20180417',
                    disables="1"
                )
             ]
        )
    )


@ntalk.callback(['ElementListCardView'])
def show_element_list_card_view(event):
    user_id = event.user_id
    ntalk.send(
        user_id,
        message=Template.CompositeContent(
            composite_list=[
                Template.Composite(
                    title='엘리먼트 리스트 카드뷰 1',
                    description='element는 3개까지 가능',
                    element_list=Template.ElementList(
                        data=[
                            Template.ElementData(
                                title='쓰레드 넘김',
                                description='파트너에게 쓰레드를 넘긴다',
                                sub_description='그러면 standby는 True',
                                button=Button.ButtonText('쓰레드 넘김', 'PassThread')
                            ),
                            Template.ElementData(
                                title='타이핑 액션',
                                description='다른 입력이 들어오면 꺼진다',
                                sub_description='10초간 지속된다.',
                                button=Button.ButtonText('타이핑 액션', 'TYPING_ON')
                            ),
                            Template.ElementData(
                                title='프로필 보기',
                                description='프로필 이벤트가 발생한다.',
                                sub_description='이벤트로 발생해서 사용하기 어려움...',
                                button=Button.ButtonText('프로필 보기', 'Profile')
                            ),
                        ]
                    )
                ),
                Template.Composite(
                    title='엘리먼트 리스트 카드뷰 2',
                    description='element는 3개까지 가능',
                    element_list=Template.ElementList(
                        data=[
                            Template.ElementData(
                                title='nta 깃헙 페이지',
                                description='파이썬 개발시 용이하다',
                                sub_description='쓸만하다',
                                button=Button.ButtonLink('nta github page', 'https://github.com/HwangWonYo/naver_talk_sdk'),
                            ),
                            Template.ElementData(
                                title='파트너 센터 페이지',
                                description='네이버 톡톡 챗봇의 시작',
                                sub_description='계정은 각자 만들어야 한다',
                                button=Button.ButtonLink('네이버 파트너 센터', 'https://partner.talk.naver.com/'),
                            ),
                            Template.ElementData(
                                title='카드뷰',
                                description='카드뷰로 보여준다',
                                sub_description='사용은 각자에게 달려있다',
                                button=Button.ButtonText('카드뷰', 'CardView')
                            ),
                        ]
                    )
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
    )
    ntalk.send(
        user_id,
        "쓰레드 넘기기 성공\n"
        "따라하기 기능이 불가능합니다."
    )


@ntalk.callback(['TakeThread'])
def thread_take(event):
    print('take thread')
    user_id = event.user_id
    ntalk.take_thread(
        user_id=user_id,
    )
    ntalk.send(
        user_id,
        "쓰레드 반환 받기 성공\n"
        "다시 따라하기 기능이 가능합니다."
    )


@ntalk.callback(['Profile'])
def show_profile(event):
    user_id = event.user_id
    ntalk.request_profile(
        user_id,
        field="nickname",
        agreements=["cellphone", "address"]
    )


@ntalk.handle_friend
def friend_event_handler(event):
    user_id = event.user_id
    if event.set_on:
        message = "친구추가해줘서 고마워"
    else:
        message = "우정이 이렇게 쉽게 깨지는 거였나.."

    ntalk.send(user_id, message)


@ntalk.handle_handover
def hand_over_handler(event):
    user_id = event.user_id
    ntalk.send(
        user_id,
        "이제 주도권은 나의 손에!"
    )


@ntalk.handle_profile
def profile_handler(event):
    user_id = event.user_id
    nickname = event.nickname
    ntalk.send(
        user_id,
        "안녕 {}".format(nickname)
    )


@ntalk.after_send
def do_something_after_send(res, payload):
    print('* Message Type: %s' % payload.__class__.__name__)


if __name__ == "__main__":
    app.run()