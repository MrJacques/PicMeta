# MIT License
#
# Copyright (c) 2020 Jacques Parker  copyright@judyandjacques.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest

from PicMeta import PicMeta


class MockFile:
    """ Just need to mock file.name (this simpler than using MagicMock """
    def __init__(self, name):
        self.file_name = name

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.file_name


class MockExifParser:
    """ Mock the exif.Image class.  Supports dir and     """

    data = {}

    @staticmethod
    def add(img_file, values: dict):
        """ add metadata.  values should be a dictionary of (label, value) """
        MockExifParser.data[img_file] = values

    def __init__(self, img_file):
        self.img_file = img_file

    @property
    def img_metadata(self):
        assert self.img_file in MockExifParser.data, '"%s" not found in mock data' % self.img_file
        return MockExifParser.data[self.img_file]

    def __dir__(self):
        for label in self.img_metadata.keys():
            yield label

    def __getitem__(self, item):
        return self.img_metadata[item]


class PicMetaTest(unittest.TestCase):
    """ Unit test for PicMeta """

    def test_contains_substring(self):
        string = "the quick brown fox"

        self.assertRaises(TypeError, lambda: PicMeta.contains_substring())
        self.assertRaises(TypeError, lambda: PicMeta.contains_substring(string))
        self.assertRaises(AssertionError, lambda: PicMeta.contains_substring(string, 'string not list'))
        self.assertFalse(PicMeta.contains_substring("", []))
        self.assertTrue(PicMeta.contains_substring(string, []))
        self.assertFalse(PicMeta.contains_substring("", ['dog']))
        self.assertRaises(AssertionError, lambda: PicMeta.contains_substring(string, ['']))
        self.assertRaises(AssertionError, lambda: PicMeta.contains_substring(string, ['dog', '']))
        self.assertRaises(AssertionError, lambda: PicMeta.contains_substring(string, ['fox', '']))
        self.assertFalse(PicMeta.contains_substring(string, ['dog']))
        self.assertTrue(PicMeta.contains_substring(string, ['the']))
        self.assertTrue(PicMeta.contains_substring(string, ['quick']))
        self.assertTrue(PicMeta.contains_substring(string, ['brown']))
        self.assertTrue(PicMeta.contains_substring(string, ['fox']))
        self.assertTrue(PicMeta.contains_substring(string, ['dog', 'fox']))
        self.assertTrue(PicMeta.contains_substring(string, ['quick', 'fox']))
        self.assertFalse(PicMeta.contains_substring(string, ['Fox']))

    def setUp(self) -> None:
        self.file_1 = MockFile('abc.jpg')
        self.file_2 = MockFile('def.jpg')
        self.file_3 = MockFile('xyz.jpg')
        self.file_4 = MockFile('xyz.jpg')

        MockExifParser.add(self.file_1, {'shared': 'abc_shared', 'abc_only': 'abc only'})
        MockExifParser.add(self.file_2, {'shared': 'def_shared', 'def_only': 'def only'})
        MockExifParser.add(self.file_3, {'shared': 'hij shared', 'hij_only': 'hij only'})

    def test_get_metadata_no_files(self):
        self.assertRaises(AssertionError, lambda: PicMeta(MockExifParser).get_metadata([], ['label']))

    def test_file_not_found(self):
        self.assertRaises(AssertionError, lambda: PicMeta(MockExifParser).get_metadata([self.file_4], []))
        self.assertRaises(AssertionError, lambda: PicMeta(MockExifParser).get_metadata([self.file_4], ['']))

    def test_get_metadata_file_1(self):
        result = PicMeta(MockExifParser).get_metadata([self.file_1], [])
        expected = {'abc.jpg': {'abc_only': 'abc only', 'shared': 'abc_shared'}}
        self.assertEqual(result, expected, 'Expected all meta data for file_1')

        result = PicMeta(MockExifParser).get_metadata([self.file_1], ['shared'])
        expected = {'abc.jpg': {'shared': 'abc_shared'}}
        self.assertEqual(result, expected, 'Expected shared meta data for file_1')

        result = PicMeta(MockExifParser).get_metadata([self.file_1], ['abc'])
        expected = {'abc.jpg': {'abc_only': 'abc only'}}
        self.assertEqual(result, expected, 'Expected abc only meta data for file_1')

        result = PicMeta(MockExifParser).get_metadata([self.file_1], ['abc_only'])
        expected = {'abc.jpg': {'abc_only': 'abc only'}}
        self.assertEqual(result, expected, 'Expected abc meta data for file_1')

        result = PicMeta(MockExifParser).get_metadata([self.file_1], ['abc', 'sh'])
        expected = {'abc.jpg': {'abc_only': 'abc only', 'shared': 'abc_shared'}}
        self.assertEqual(result, expected, 'Expected abc only and shared meta data for file_1')

        result = PicMeta(MockExifParser).get_metadata([self.file_1], ['not there'])
        expected = {'abc.jpg': {}}
        self.assertEqual(result, expected, 'Expected no meta data for file_1')

        self.assertRaises(AssertionError, lambda: PicMeta(MockExifParser).get_metadata([self.file_1], ['']))

    def test_get_metadata_file_2(self):
        result = PicMeta(MockExifParser).get_metadata([self.file_2], [])
        expected = {'def.jpg': {'def_only': 'def only', 'shared': 'def_shared'}}
        self.assertEqual(result, expected, 'Expected all meta data for file_2')

        result = PicMeta(MockExifParser).get_metadata([self.file_2], ['shared'])
        expected = {'def.jpg': {'shared': 'def_shared'}}
        self.assertEqual(result, expected, 'Expected shared meta data for file_2')

        result = PicMeta(MockExifParser).get_metadata([self.file_2], ['def'])
        expected = {'def.jpg': {'def_only': 'def only'}}
        self.assertEqual(result, expected, 'Expected def only meta data for file_2')

        result = PicMeta(MockExifParser).get_metadata([self.file_2], ['def_only'])
        expected = {'def.jpg': {'def_only': 'def only'}}
        self.assertEqual(result, expected, 'Expected def meta data for file_2')

        result = PicMeta(MockExifParser).get_metadata([self.file_2], ['def', 'sh'])
        expected = {'def.jpg': {'def_only': 'def only', 'shared': 'def_shared'}}
        self.assertEqual(result, expected, 'Expected def only and shared meta data for file_2')

        result = PicMeta(MockExifParser).get_metadata([self.file_2], ['not there'])
        expected = {'def.jpg': {}}
        self.assertEqual(result, expected, 'Expected no meta data for file_2')

        self.assertRaises(AssertionError, lambda: PicMeta(MockExifParser).get_metadata([self.file_2], ['']))

    def test_get_metadata_file_both(self):
        result = PicMeta(MockExifParser).get_metadata([self.file_1, self.file_2], [])
        expected = {'abc.jpg': {'abc_only': 'abc only', 'shared': 'abc_shared'},
                    'def.jpg': {'def_only': 'def only', 'shared': 'def_shared'}}
        self.assertEqual(result, expected, 'Expected all meta data')

        result = PicMeta(MockExifParser).get_metadata([self.file_1, self.file_2], ['shared'])
        expected = {'abc.jpg': {'shared': 'abc_shared'}, 'def.jpg': {'shared': 'def_shared'}}
        self.assertEqual(result, expected, 'Expected shared meta data')

        result = PicMeta(MockExifParser).get_metadata([self.file_1, self.file_2], ['def'])
        expected = {'abc.jpg': {}, 'def.jpg': {'def_only': 'def only'}}
        self.assertEqual(result, expected, 'Expected def only meta data')

        result = PicMeta(MockExifParser).get_metadata([self.file_1, self.file_2], ['def_only'])
        expected = {'abc.jpg': {}, 'def.jpg': {'def_only': 'def only'}}
        self.assertEqual(result, expected, 'Expected def only')

        result = PicMeta(MockExifParser).get_metadata([self.file_1, self.file_2], ['def', 'sh'])
        expected = {'abc.jpg': {'shared': 'abc_shared'}, 'def.jpg': {'def_only': 'def only', 'shared': 'def_shared'}}
        self.assertEqual(result, expected, 'Expected def only and shared meta data')

        result = PicMeta(MockExifParser).get_metadata([self.file_1, self.file_2], ['not there'])
        expected = {'abc.jpg': {}, 'def.jpg': {}}
        self.assertEqual(result, expected, 'Expected no meta data for file_2')

        self.assertRaises(AssertionError,
                          lambda: PicMeta(MockExifParser).get_metadata([self.file_1, self.file_2], ['']))


if __name__ == '__main__':
    unittest.main()
