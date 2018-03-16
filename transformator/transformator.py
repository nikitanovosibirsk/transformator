from .path import Path
from .transformation import Transformation
from .wrapper import Wrapper


class Transformator:
    def __init__(self, transformations):
        self._transformations = transformations

    def _traverse(self, path, container, handler):
        if isinstance(container, dict):
            return handler(path, {
                key: self._traverse(path + key, val, handler)
                    for key, val in container.items()
            })
        elif isinstance(container, list):
            return handler(path, [
                self._traverse(path + idx, elem, handler)
                    for idx, elem in enumerate(container)
            ])
        else:
            return handler(path, container)

    def _traverse_tf(self, node, handler):
        handler(node)
        return [self._traverse_tf(child, handler) for _, child in node.items()]

    def transform(self, container):
        wrapper = Wrapper()
        paths = []

        def handler(path, val):
            handlers = self._transformations.find(path)
            if len(handlers) > 0:
                for handler in handlers:
                    new_path, new_val = handler(path, val)
                    wrapper.insert(Path(new_path), new_val)
            paths.append(path)
            return val

        self._traverse(Path(), container, handler)

        def tf_handler(node):
            if not node.optional and node.path not in paths:
                raise KeyError(str(node.path))

        self._traverse_tf(self._transformations, tf_handler)

        return wrapper.val()
