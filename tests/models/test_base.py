#-*- encoding:utf8 -*-
from __future__ import unicode_literals, absolute_import

import unittest

from nta.models import (
    Base, events
)
from nta import Template


class TestBaseTemplate(unittest.TestCase):

    def test_convert_to_camel_case(self):
        camel_case_dict = Base.convert_dict_to_camel_case(
            {
                "event": "send",
                "user": "al-2eGuGr5WQOnco1_V-FQ",
                "text_content": {
                    "text": "hello world",
                    "input_type": "typing"
                }
            }
        )
        self.assertEqual(
            camel_case_dict,
            {
                "event": "send",
                "user": "al-2eGuGr5WQOnco1_V-FQ",
                "textContent": {
                    "text": "hello world",
                    "inputType": "typing"
                }
            }
        )
        camel_case_dict = Base.convert_dict_to_camel_case(
            {
                "event": "send",
                "user": "al-2eGuGr5WQOnco1_V-FQ",
                "text_content": Template.TextContent('Test_text', 'Test_Code')
            }
        )
        self.assertEqual(
            camel_case_dict,
            {
                "event": "send",
                "user": "al-2eGuGr5WQOnco1_V-FQ",
                "textContent": {
                    "text": "Test_text",
                    "code": "Test_Code",
                    "inputType": None
                }
            }
        )

    def test_dict_to_snake_case(self):
        snake_case_dict = Base.dict_to_snake_case(
            {
                "camelCaseKey": {
                    "insideCamelCaseDict":{
                        "againInsideCamelCaseDict": "valueDoNotChangeIntoSnakeCase"
                    }
                }
            }
        )
        self.assertEqual(
            snake_case_dict,
            {
                "camel_case_key":{
                    "inside_camel_case_dict": {
                        "again_inside_camel_case_dict": "valueDoNotChangeIntoSnakeCase"
                    }
                }
            }
        )

    def test_new_from_json_dict(self):
        new_event = events.LeaveEvent.new_from_json_dict(
            {
                "event": "leave",
                "user": "al-2eGuGr5WQOnco1_V-FQ"
            }

        )
        self.assertTrue(isinstance(new_event, events.LeaveEvent))

    def test_others(self):
        new_event = events.LeaveEvent.new_from_json_dict(
            {
                "event": "leave",
                "user": "al-2eGuGr5WQOnco1_V-FQ"
            }

        )
        self.assertEqual(str(new_event), new_event.as_json_string())
        self.assertEqual(str(new_event), repr(new_event))
        self.assertTrue(new_event == new_event.as_json_dict())
        self.assertTrue(new_event == str(new_event))
        self.assertFalse(new_event != new_event)




if __name__ == '__main__':
    unittest.main()