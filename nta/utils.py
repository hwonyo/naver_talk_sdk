# -*- coding: utf-8 -*-
import logging
import re
import sys

LOGGER = logging.getLogger('nta')

PY3 = sys.version_info[0] == 3


def to_snake_case(text):
    """Convert to snake case.
    :param str text:
    :rtype: str
    :return:
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def to_camel_case(text):
    """Convert to camel case.
    :param str text:
    :rtype: str
    :return:
    """
    split = text.split('_')
    return split[0] + "".join(x.title() for x in split[1:])


def _byteify(input):
    """Encoding UTF-8
    :param input: unicode
    :rtype: str
    :return:
    """
    if isinstance(input, dict):
        return {_byteify(key): _byteify(value)
                for key, value in input.items()}
    elif isinstance(input, list):
        return [_byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input