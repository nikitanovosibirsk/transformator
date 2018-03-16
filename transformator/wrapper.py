class Wrapper:
    def __init__(self):
        self._container = None

    def _insert(self, pointer, path, val):
        if len(path) == 1:
            if path[0] == int:
                pointer += [val]
            else:
                pointer[path[0]] = val

        elif (path[0] != int) and (path[1] != int):
            if path[0] in pointer:
                self._insert(pointer[path[0]], path[1:], val)
            else:
                pointer[path[0]] = self._insert({}, path[1:], val)

        elif (path[0] != int) and (path[1] == int):
            if path[0] in pointer:
                self._insert(pointer[path[0]], path[1:], val)
            else:
                pointer[path[0]] = self._insert([], path[1:], val)

        elif (path[0] == int) and (path[1] != int):
            if (len(pointer) > 0) and (path[1] not in pointer[-1]):
                self._insert(pointer[-1], path[1:], val)
            else:
                pointer.append(self._insert({}, path[1:], val))

        else:
            raise TypeError

        return pointer

    def insert(self, path, val):
        if self._container is None:
            self._container = [] if (path[0] == int) else {}
        
        self._container = self._insert(self._container, path, val)

        return self

    def val(self):
        return self._container

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self._container if self._container is not None else ''
        )
