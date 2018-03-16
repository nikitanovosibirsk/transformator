from re import findall, split


class Path:
    def __init__(self, parts = None, separator = '.', root = '#'):
        self._root = root
        self._separator = separator
        if isinstance(parts, str):
            self._parts = self._from_str(parts)
        elif isinstance(parts, list):
            self._parts = self._from_list(parts)
        else:
            self._parts = []

    @property
    def separator(self):
        return self._separator

    @property
    def root(self):
        return self._root

    def _split(self, composite_key):
        pattern = r'(?<!\\)' + '\\' + self._separator
        return split(pattern, composite_key) if isinstance(composite_key, str) else [composite_key]

    def _join(self, parts):
        return self._separator.join(parts)

    def _match(self, part):
        matches = findall(r'\[(\d*)\]$', part)
        if len(matches) == 0:
            return part, None
        elif len(matches[0]) == 0:
            return part[:-2], int
        else:
            return part[:-2-len(matches[0])], int(matches[0])

    def _from_str(self, composite_key):
        parts = []
        for part in self._split(composite_key):
            key, index = self._match(part)
            if len(key) > 0:
                parts += [key]
            if index is not None:
                parts += [index]
        return self._from_list(parts)

    def _from_list(self, parts):
        return parts

    def __add__(self, part):
        if part == int:
            return Path(self._parts + [int])
        elif isinstance(part, int):
            return Path(self._parts + [part])
        return Path(self._parts + self._from_str(part))

    def __iadd__(self, part):
        if part == int:
            self._parts += [int]
        elif isinstance(part, int):
            self._parts += [part]
        else:
            self._parts += self._from_str(part)
        return self

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Path(self._parts[key.start:key.stop:key.step])
        elif isinstance(key, int):
            return self._parts[key]
        raise TypeError

    def __str__(self):
        path = self._root
        for part in self._parts:
            if part == int:
                formatted = '[]'
            elif isinstance(part, int):
                formatted = '[{}]'.format(part)
            else:
                formatted = self._separator + '{}'.format(part)
            path += formatted
        return path

    def __iter__(self):
        yield from self._parts

    def __len__(self):
        return len(self._parts)

    def __eq__(self, other):
        if (self._separator != other.separator) or (self._root != other.root):
            return False
        if len(self._parts) != len(other):
            return False
        for idx, part in enumerate(other):
            if (part == int):
                if (self._parts[idx] != int) and (not isinstance(self._parts[idx], int)):
                    return False
            elif (self._parts[idx] == int):
                if (part != int) and (not isinstance(part, int)):
                    return False
            elif part != self._parts[idx]:
                return False
        return True

    def __repr__(self):
        if (self._separator != '.') and (self._root != '#'):
            return 'Path({}, separator=\'{}\', root=\'{}\')'.format(self._parts, self._separator, self._root)
        elif self._separator != '.':
            return 'Path({}, separator=\'{}\')'.format(self._parts, self._separator)
        elif self._root != '#':
            return 'Path({}, root=\'{}\')'.format(self._parts, self._root)
        else:
            return 'Path({})'.format(self._parts)
