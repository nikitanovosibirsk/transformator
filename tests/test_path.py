from typing import Generator
from unittest import TestCase

from transformator.path import Path


class TestPath(TestCase):
    def test_move_str_part(self):
        path = Path()
        moved = path + 'key1'
        self.assertNotEqual(path, moved)
        self.assertEqual(list(moved), ['key1'])
        
        path = Path()
        path += 'key1'
        self.assertEqual(list(path), ['key1'])

    def test_move_str_part_with_str_initial(self):
        path = Path(['key0'])
        moved = path + 'key1'
        self.assertNotEqual(path, moved)
        self.assertEqual(list(moved), ['key0', 'key1'])

        path = Path(['key0'])
        path += 'key1'
        self.assertEqual(list(path), ['key0', 'key1'])

    def test_move_str_part_with_int_initial(self):
        path = Path([0])
        moved = path + 'key1'
        self.assertNotEqual(path, moved)
        self.assertEqual(list(moved), [0, 'key1'])

        path = Path([0])
        path += 'key1'
        self.assertEqual(list(path), [0, 'key1'])

    def test_move_int_part(self):
        path = Path()
        moved = path + 1
        self.assertNotEqual(path, moved)
        self.assertEqual(list(moved), [1])

        path = Path()
        path += 1
        self.assertEqual(list(path), [1])

    def test_move_int_part_with_int_initial(self):
        path = Path([0])
        moved = path + 1
        self.assertNotEqual(path, moved)
        self.assertEqual(list(moved), [0, 1])

    def test_move_int_part_with_str_initial(self):
        path = Path(['key0'])
        moved = path + 1
        self.assertNotEqual(path, moved)
        self.assertEqual(list(moved), ['key0', 1])

    def test_iter(self):
        self.assertIsInstance(iter(Path()), Generator)

    def test_empty_list_parts(self):
        parts = []
        path = Path(parts)
        self.assertEqual(list(path), parts)

    def test_list_parts(self):
        path = Path(['key0'])
        self.assertEqual(list(path), ['key0'])

        path = Path(['key0', 'key1'])
        self.assertEqual(list(path), ['key0', 'key1'])

        path = Path(['key0', 'key1', 0])
        self.assertEqual(list(path), ['key0', 'key1', 0])

        path = Path(['key0', 'key1', 0, 'key2'])
        self.assertEqual(list(path), ['key0', 'key1', 0, 'key2'])

        path = Path(['key0', 'key1', int])
        self.assertEqual(list(path), ['key0', 'key1', int])

        path = Path(['key0', 'key1', int, 'key2'])
        self.assertEqual(list(path), ['key0', 'key1', int, 'key2'])

    def test_empty_str_parts(self):
        path = Path('')
        self.assertEqual(list(path), [])

    def test_str_parts(self):
        path = Path('key0')
        self.assertEqual(list(path), ['key0'])

        path = Path('key0.key1')
        self.assertEqual(list(path), ['key0', 'key1'])

        path = Path('key0.key1[0]')
        self.assertEqual(list(path), ['key0', 'key1', 0])

        path = Path('key0.key1[10]')
        self.assertEqual(list(path), ['key0', 'key1', 10])

        path = Path('key0.key1[0].key2')
        self.assertEqual(list(path), ['key0', 'key1', 0, 'key2'])

        path = Path('key0.key1[]')
        self.assertEqual(list(path), ['key0', 'key1', int])

        path = Path('key0.key1[].key2')
        self.assertEqual(list(path), ['key0', 'key1', int, 'key2'])

    def test_separator(self):
        path = Path([], separator='_')
        self.assertEqual(path.separator, '_')

        path = Path('key0_key1', separator='_')
        self.assertEqual(list(path), ['key0', 'key1'])

    def test_root(self):
        path = Path([], root='@')
        self.assertEqual(path.root, '@')

        path = Path(['key0', 'key1'], root='@')
        self.assertEqual(list(path), ['key0', 'key1'])

    def test_equal(self):
        path1 = Path([])
        path2 = Path('')
        self.assertEqual(path1, path2)

        path1 = Path(['key0', 'key1', 0])
        path2 = Path(['key0', 'key1', 0])
        self.assertEqual(path1, path2)

        path1 = Path(['key0', 'key1', 0])
        path2 = Path('key0.key1[0]')
        self.assertEqual(path1, path2)

        path1 = Path(['key0', 'key1', 0, 'key2'])
        path2 = Path('key0.key1[0].key2')
        self.assertEqual(path1, path2)

        path1 = Path(['key0', 'key1', int, 'key2'])
        path2 = Path('key0.key1[].key2')
        self.assertEqual(path1, path2)

        path1 = Path(['key0', 'key1', int, 'key2'])
        path2 = Path('key0.key1[0].key2')
        self.assertEqual(path1, path2)

        path1 = Path(['key0', 'key1', 0, 'key2'])
        path2 = Path('key0.key1[].key2')
        self.assertEqual(path1, path2)

    def test_not_equal(self):
        path1 = Path([])
        path2 = Path(['key0'])
        self.assertNotEqual(path1, path2)

        path1 = Path(['key0', 'key1', 0, 'key2'])
        path2 = Path(['key0', 'key1', 0])
        self.assertNotEqual(path1, path2)

        path1 = Path(['key0', 'key1', 0])
        path2 = Path(['key1', 'key0', 0])
        self.assertNotEqual(path1, path2)

        path1 = Path(['key0', 'key1', 0])
        path2 = Path(['key0', 'key1', 1])
        self.assertNotEqual(path1, path2)

        path1 = Path(['key0', 'key1', 0])
        path2 = Path(['key0', 'key1', 0], separator='_')
        self.assertNotEqual(path1, path2)

        path1 = Path(['key0', 'key1', 0])
        path2 = Path(['key0', 'key1', 0], root='@')
        self.assertNotEqual(path1, path2)

    def test_slicing(self):
        path = Path()
        with self.assertRaises(IndexError):
            Path()[0]

        path = Path(['key0', 0, 'key1'])
        self.assertEqual(path[0], 'key0')
        self.assertEqual(list(path[1:-1]), [0])

    def test_type_cast(self):
        self.assertEqual(str(Path()), '#')
        self.assertEqual(str(Path([])), '#')

        path = Path(['key0', 'key1', 0, 'key2'])
        self.assertEqual(str(path), '#.key0.key1[0].key2')

        path = Path([0, 'key0', 1, 'key2'])
        self.assertEqual(str(path), '#[0].key0[1].key2')

        path = Path(['key0', 'key1', 0, 'key2'], separator='_')
        self.assertEqual(str(path), '#_key0_key1[0]_key2')

        path = Path(['key0', 'key1', 0, 'key2'], root='@')
        self.assertEqual(str(path), '@.key0.key1[0].key2')

        path = Path(['key0', 'key1', 0, 'key2'], separator='_', root='@')
        self.assertEqual(str(path), '@_key0_key1[0]_key2')

    def test_repr(self):
        self.assertEqual(repr(Path()), "Path([])")

        path = Path(['key0', 'key1', 0, 'key2'])
        self.assertEqual(repr(path), "Path(['key0', 'key1', 0, 'key2'])")
        
        path = Path([0, 'key0', 1, 'key2'])
        self.assertEqual(repr(path), "Path([0, 'key0', 1, 'key2'])")

        path = Path(['key0', 'key1', 0, 'key2'], separator=',')
        self.assertEqual(repr(path), "Path(['key0', 'key1', 0, 'key2'], separator=',')")

        path = Path(['key0', 'key1', 0, 'key2'], root='@')
        self.assertEqual(repr(path), "Path(['key0', 'key1', 0, 'key2'], root='@')")

        path = Path(['key0', 'key1', 0, 'key2'], separator=',', root='@')
        self.assertEqual(repr(path), "Path(['key0', 'key1', 0, 'key2'], separator=',', root='@')")
