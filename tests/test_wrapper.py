from unittest import TestCase

from transformator.path import Path
from transformator.wrapper import Wrapper


class TestWrapper(TestCase):
    def assertInserted(self, paths, expected):
        wrapper = Wrapper()
        for idx, path in enumerate(paths):
            wrapper.insert(Path(path), idx + 1)
        actual = wrapper.val()
        self.assertEqual(actual, expected)

    def test_initial_dict(self):
        self.assertInserted(['key1'], {'key1': 1})

    def test_initial_list(self):
        self.assertInserted(['[]'], [1])

    def test_insert_single_path(self):
        self.assertInserted(['key1'], {'key1': 1})
        self.assertInserted(['key1.key2'], {'key1': {'key2': 1}})
        self.assertInserted(['key1.key2.key3'], {'key1': {'key2': {'key3': 1}}})

        self.assertInserted(['[]'], [1])
        self.assertInserted(['[].key1'], [{'key1': 1}])
        self.assertInserted(['[].key1[]'], [{'key1': [1]}])
        self.assertInserted(['[].key1[].key2'], [{'key1': [{'key2': 1}]}])
        self.assertInserted(['[].key1[].key2.key3'], [{'key1': [{'key2': {'key3': 1}}]}])

        self.assertInserted(['key1[]'], {'key1': [1]})
        self.assertInserted(['key1[].key2'], {'key1': [{'key2': 1}]})
        self.assertInserted(['key1[].key2[]'], {'key1': [{'key2': [1]}]})
        self.assertInserted(['key1[].key2[].key3'], {'key1': [{'key2': [{'key3': 1}]}]})
        self.assertInserted(['key1[].key2[].key3[]'], {'key1': [{'key2': [{'key3': [1]}]}]})

        self.assertInserted(['key1.key2[]'], {'key1': {'key2': [1]}})
        self.assertInserted(['key1.key2[].key3'], {'key1': {'key2': [{'key3': 1}]}})
        self.assertInserted(['key1.key2[].key3.key4[]'], {'key1': {'key2': [{'key3': {'key4': [1]}}]}})

    def test_insert_multiple_path(self):
        self.assertInserted(['key1', 'key2'], {'key1': 1, 'key2': 2})
        self.assertInserted(['key1[]', 'key2[]'], {'key1': [1], 'key2': [2]})

        self.assertInserted(['key1.key2', 'key1.key3'], {'key1': {'key2': 1, 'key3': 2}})
        self.assertInserted(['key1[].key2', 'key1[].key3'], {'key1': [{'key2': 1, 'key3': 2}]})

        # self.assertInserted(['key1[].key2.key3', 'key1[].key2.key4'], {'key1': [{'key2': {'key3': 1, 'key4': 2}}]})

    def test_repr(self):
        wrapper = Wrapper()
        self.assertEqual(str(wrapper), 'Wrapper()')
