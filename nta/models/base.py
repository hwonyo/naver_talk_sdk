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
        for key in self.__dict__.keys():
            camel_key = utils.to_camel_case(key)
            if isinstance(getattr(self, key, None), (list, tuple, set)):
                data[camel_key] = list()
                for sub_obj in getattr(self, key, None):
                    if hasattr(sub_obj, 'as_json_dict'):
                        data[camel_key].append(sub_obj.as_json_dict())
                    elif isinstance(sub_obj, dict):
                        data[camel_key].append(self.convert_dict_to_camel_case(sub_obj))
                    else:
                        data[camel_key].append(sub_obj)

            elif isinstance(getattr(self, key, None), dict):
                data[camel_key] = self.convert_dict_to_camel_case(getattr(self, key))

            elif hasattr(getattr(self, key, None), 'as_json_dict'):
                data[camel_key] = getattr(self, key).as_json_dict()

            else:
                data[camel_key] = getattr(self, key, None)

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

    @staticmethod
    def get_or_new_from_json_dict(data, cls):
        """Get `cls` object w/ deserialization from json if needed.
        If data is instance of cls, return data.
        Else if data is instance of dict, create instance from dict.
        Else, return None.
        :param data:
        :param cls:
        :rtype: object
        :return:
        """
        if isinstance(data, cls):
            return data
        elif isinstance(data, dict):
            return cls.new_from_json_dict(data)

        return None

    @staticmethod
    def get_or_new_from_json_dict_with_types(
            data, cls_map, type_key='type'
    ):
        """Get `cls` object w/ deserialization from json by using type key hint if needed.
        If data is instance of one of cls, return data.
        Else if data is instance of dict, create instance from dict.
        Else, return None.
        :param data:
        :param cls_map:
        :param type_key:
        :rtype: object
        :return:
        """
        if isinstance(data, tuple(cls_map.values())):
            return data
        elif isinstance(data, dict):
            type_val = data[type_key]
            if type_val in cls_map:
                return cls_map[type_val].new_from_json_dict(data)

        return None
