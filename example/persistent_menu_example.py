#-*- encoding:utf-8 -*-
"""
     In Persistent Menu,
     Option Button is not allowed.
     Sad..

     How to register persistent menu:
     python persistent_menu_example.py

"""
import os

from nta import NaverTalkApi, Button

NAVER_TALK_ACCESS_TOKEN = os.environ['naver_talk_access_token']
ntalk = NaverTalkApi(NAVER_TALK_ACCESS_TOKEN)

def my_callback(res, payload):
    #callback function for showing result of send persistent menu payload
    print(res)

ntalk.persistent_menu(
    menus=[
        Button.ButtonText(
            '고정 메뉴 테스트',
            'PersistentMenu'
        ),
        Button.ButtonLink(
            'Link to NTA',
            'https://github.com/HwangWonYo/naver_talk_sdk'
        ),
        Button.ButtonNested(
            title='버튼을 품은 버튼 이라는데?',
            menus=[
                Button.ButtonText('아무 의미 없는 버튼'),
                Button.ButtonText('카드뷰 보기', 'CardView'),
            ]
        )
    ],
    callback=my_callback
)