#! /usr/bin/env python
import unittest
import isoparser

from isoparser.test.test_data import TEST_DATA


class TestIso(unittest.TestCase):
    def recursive_test_record(self, record, content):
        self.assertTrue(record.is_directory)
        self.assertEqual(len(record.children), len(content))

        for child in record.children:
            self.assertIn(child.name, content)
            value = content[child.name]
            if child.is_directory:
                self.recursive_test_record(child, value)
            else:
                self.assertEqual(child.content, value)

    def test_root(self):
        for filename, content in TEST_DATA:
            iso = isoparser.parse(filename)
            self.assertEqual(len(iso.root.children), len(content))
            self.recursive_test_record(iso.root, content)
            iso.close()
