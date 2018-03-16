from .path import Path
from .transformation import Transformation
from .wrapper import Wrapper


class tf:
    namespaces = {}

    def __init__(self, old_path, new_path):
        self._old_path = old_path
        self._new_path = new_path

    def _register_handler(self, fn):
        namespace = fn.__module__ + '.' + fn.__qualname__[:-len(fn.__name__) - 1]
        if namespace not in self.namespaces:
            self.namespaces[namespace] = {}

        if type(self._new_path) == type(Transformator):
            ns = self._new_path.__module__ + '.' + self._new_path.__qualname__
            separator = self._new_path.separator
            keys = self.namespaces.get(ns)
            new_keys = {}
            for key, val in keys.items():
                new_key = self._old_path + separator + key
                new_keys[new_key] = val
            self.namespaces[namespace].update(new_keys)
        else:
            self.namespaces[namespace][self._old_path] = lambda path, val: (self._new_path, fn(path, val))

        return namespace

    def __call__(self, fn):
        self._register_handler(fn)
        return fn


class Transformator:
    separator = '.'
    tf = tf

    def __traverse(self, path, container, handler):
        if isinstance(container, dict):
            return handler(path, {
                key: self.__traverse(path + key, val, handler)
                    for key, val in container.items()
            })
        elif isinstance(container, list):
            return handler(path, [
                self.__traverse(path + idx, elem, handler)
                    for idx, elem in enumerate(container)
            ])
        else:
            return handler(path, container)

    def __traverse_tf(self, node, handler):
        handler(node)
        return [self.__traverse_tf(child, handler) for _, child in node.items()]

    @property
    def namespace(self):
        return '{module}.{name}'.format(
            module=self.__class__.__module__,
            name=self.__class__.__name__
        )

    def transform(self, container):
        keys = self.tf.namespaces.get(self.namespace)
        tree = Transformation.from_dict(keys, Path())

        wrapper = Wrapper()
        paths = []

        def handler(path, val):
            handlers = tree.find(path)
            if len(handlers) > 0:
                for handler in handlers:
                    new_path, new_val = handler(path, val)
                    wrapper.insert(Path(new_path), new_val)
            paths.append(path)
            return val

        self.__traverse(Path(), container, handler)

        def tf_handler(node):
            if not node.optional and node.path not in paths:
                raise KeyError(str(node.path))

        self.__traverse_tf(tree, tf_handler)

        return wrapper.val()
