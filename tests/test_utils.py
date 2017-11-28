from __future__ import unicode_literals, absolute_import

import unittest

from nta.utils import to_camel_case, to_snake_case, _byteify, PY3


class TestUtils(unittest.TestCase):
    def test_to_snake_case(self):
        self.assertEqual(to_snake_case('hogeBar'), 'hoge_bar')

    def test_to_camel_case(self):
        self.assertEqual(to_camel_case('hoge_bar'), 'hogeBar')

    def test__byteify(self):
        if not PY3:
            self.assertEqual(_byteify(u'test'), str('test'))
            self.assertEqual(_byteify([u'test', u'test2']), [str('test'), str('test2')])
            self.assertEqual(_byteify({u'test_key': u'test_value'}), {str('test_key'): str('test_value')})


if __name__ == '__main__':
    unittest.main()