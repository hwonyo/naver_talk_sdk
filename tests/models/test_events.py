#-*- encoding:utf8 -*-
from __future__ import unicode_literals, absolute_import

import unittest

from nta.models import (
    Base, events
)

class TestNaverTalkEvent(unittest.TestCase):
    def test_echo_event(self):
        event = {
            "standby": True,
            "event": "send",
            "user": "al-2eGuGr5WQOnco1_V-FQ",
            "partner": "wc8b1i",
            "textContent": {
                "text": "헬로",
                "inputType": "typing"
            },
            "options": {
                "mobile": False
             }
        }

