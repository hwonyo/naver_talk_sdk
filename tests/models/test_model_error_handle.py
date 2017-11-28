#-*- encoding:utf8 -*-
from __future__ import unicode_literals, absolute_import

import unittest

from nta.models import (
    GenericPayload, ImageContent, Buttons
)


class TestNaverTalkApi(unittest.TestCase):

    def test_payload_error(self):
        with self.assertRaises(ValueError):
            GenericPayload({'test_key', 'test_value'}, user='test_user')

    def test_image_content_error(self):
        with self.assertRaises(TypeError) as e:
            ImageContent()

    def test_button_invalid_type_error(self):
        with self.assertRaises(ValueError):
            Buttons.convert_shortcut_buttons([{'type': 'PEY', 'value': 'test'}])

        with self.assertRaises(ValueError):
            Buttons.convert_shortcut_buttons(['test_button_text'])


if __name__ == '__main__':
    unittest.main()