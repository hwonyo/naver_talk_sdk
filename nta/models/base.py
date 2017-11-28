# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from .. import utils


class Base(object):
    """Base class of model.
    Suitable for JSON base data.
    """

    def __init__(self, **kwargs):
        """__init__ method.
        :param kwargs:
        """
        pass

    def __str__(self):
        """__str__ method.
        :return:
        """
        return self.as_json_string()

    def __repr__(self):
        """__repr__ method.
        :return:
        """
        return str(self)

    def __eq__(self, other):
        """__eq__ method.
        :param other:
        :return:
        """
        if isinstance(other, dict):
            return other == self.as_json_dict()
        return other and self.as_json_dict() == other.as_json_dict()

    def __ne__(self, other):
        """__ne__ method.
        :param other:
        :return:
        """
        return not self.__eq__(other)

    def as_json_string(self):
        """Return JSON string from this object.
        :rtype: str
        :return:
        """
        return json.dumps(self.as_json_dict(), sort_keys=True)

    def as_json_dict(self):
        """Return dictionary from this object.
        :return: dict
        """
        data = {}
        for key, sub_obj in self.__dict__.items():
            camel_key = utils.to_camel_case(key)
            if isinstance(sub_obj, (list, tuple, set)):
                data[camel_key] = list()
                for obj in sub_obj:
                    if hasattr(obj, 'as_json_dict'):
                        data[camel_key].append(obj.as_json_dict())
                    elif isinstance(obj, dict):
                        data[camel_key].append(self.convert_dict_to_camel_case(obj))
                    else:
                        data[camel_key].append(obj)

            elif isinstance(sub_obj, dict):
                data[camel_key] = self.convert_dict_to_camel_case(sub_obj)

            elif hasattr(sub_obj, 'as_json_dict'):
                data[camel_key] = sub_obj.as_json_dict()

            else:
                data[camel_key] = sub_obj

        return data

    @classmethod
    def convert_dict_to_camel_case(cls, d):
        new_d = {}
        for key, v in d.items():
            camel_key = utils.to_camel_case(key)
            if hasattr(v, 'as_json_dict'):
                new_d[camel_key] = v.as_json_dict()
            elif isinstance(v, dict):
                new_d[camel_key] = cls.convert_dict_to_camel_case(v)
            else:
                new_d[camel_key] = v
        return new_d

    @classmethod
    def new_from_json_dict(cls, data):
        """Create a new instance from a dict.
        :param data: JSON dict
        :rtype:
        :return:
        """
        new_data = cls.dict_to_snake_case(data)

        return cls(**new_data)

    @classmethod
    def dict_to_snake_case(cls, data):
        """Convert dict key into snake_case

        :param dict data:
        :return:
        """
        if isinstance(data, dict):
            new_data = {utils.to_snake_case(key): cls.dict_to_snake_case(value)
                        for key, value in data.items()}
            return new_data
        return data