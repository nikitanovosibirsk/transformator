import re
from collections import OrderedDict

from .path import Path


class Transformation:
    def __init__(self, path, optional = False, handlers = None, children = None):
        self._path = path
        self._optional = optional
        self._handlers = handlers if handlers is not None else []
        self._children = children if children is not None else {}

    @property
    def path(self):
        return self._path

    @property
    def optional(self):
        return self._optional

    def __getitem__(self, key):
        return self._children[key]

    def __setitem__(self, key, value):
        self._children[key] = value

    def __delitem__(self, key):
        del self._children[key]

    def __contains__(self, key):
        return key in self._children

    def __len__(self):
        return len(self._children)

    def items(self):
        return self._children.items()

    def find(self, path):
        if self._path == path:
            return self._handlers
        elif len(self._children) > 0:
            for _, child in self._children.items():
                res = child.find(path)
                if len(res) > 0:
                    return res
        return []

    @classmethod
    def split(cls, composite_key, separator = '.'):
        pattern = r'(?<!\\)' + '\\' + separator
        return re.split(pattern, composite_key) if isinstance(composite_key, str) else [composite_key]

    @classmethod
    def join(cls, parts: list, separator: str = '.'):
        return separator.join(parts)

    @classmethod
    def from_dict(cls, pairs, path, optional = False, handlers = []):
        node = cls(path, optional, handlers)

        if not isinstance(pairs, cls):
            pairs = OrderedDict(sorted(pairs.items()))

        for composite_key, val in pairs.items():
            head, *tail = cls.split(composite_key)
            optional = False
            if head.endswith('?'):
                head = head[:-1]
                optional = True
            if len(tail) == 0:
                node[head] = cls(path + head, optional, val)
            else:
                new_composite_key = cls.join(tail)
                if head not in node:
                    node[head] = cls(path + head, optional)
                node[head][new_composite_key] = val

        for key, val in node.items():
            node[key] = cls.from_dict(val, path + key, val.optional, node[key]._handlers)

        return node

    def __repr__(self, indent = 0):
        name = self.__class__.__name__
        optional = self._optional
        path = self._path
        handlers = [handler.__name__ for handler in self._handlers]

        keys = []
        for key, val in self._children.items():
            _repr = val.__repr__(indent=indent + 4) if isinstance(val, type(self)) else val.__repr__()
            key = '{}\'{}\': {}'.format(' ' * (indent + 4), key, _repr)
            keys += [key]
        if len(keys) > 0:
            children = '{\n' + ',\n'.join(keys) + '\n' + (' ' * indent) + '}'
        else:
            children = '{}'

        return '{}(\'{}\', {}, {}, {})'.format(name, path, optional, handlers, children)
