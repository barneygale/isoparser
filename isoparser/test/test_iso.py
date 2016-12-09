#! /usr/bin/env python
import unittest
import isoparser


class TestIso(unittest.TestCase):
    ISO_FILENAME = "isoparser/test/test.iso"
    ISO_CONTENT = {b'a': b'==> /dev/urandom <==\n\xbf\x91BL\x91\xb3$\x9cfRa\t\x8f\x88\x84\xf6\xebd\xc2:T03\xdc\xfe\x07\xe5}\xbb|?\xd7 V\xff\x98\xb7\xc6\xc8r7\x08\xcb\t\xb5\xa4\x05`\x82\xa6\x91\xee\xf8\xf3mFw/d\x95\x035\xfc\xac\x88\x1e*C\xcb\xa7',
                   b'a long name of a directory WITH some \xc5\x82\xc5\x82 UTF8 \xc4\x85\xc5\x82 characters and with some comas (,) and very long\xc5\x82': {b'rrrrcooo': b''},
                   b'a long name of a directory without any UTF8 characters, but with some comas and very long': {b'aeu': b'',
                       b'content': b'pR\xb7\x04\xc8\xd5caa\x12@o\xc0\xe6/-\xb4+b\xf5}+\x046\x9e\xf3\x13\x97\xe1r4\xc4\xe8M\xdcC\xa4\x87\x90"?\x19\xc3\xa4\x9a\xbdK\x1bq\xbb\x18\x13|\\\x89\x0bpT\x1d9m\xdd\t\xd0`g%\xead\xd3'},
                   b'a very long name': b'',
                   b'a\xc5\x82\xc3\xb3k long name with UTF characters.\xc5\x9ba\xc5\x82\xc5\x82.txt': b'',
                   b'directory': {b'test': b''},
                   b'one': b'',
                   b'something': b"\x01\x98\t\x14\x87\xc6\xee\xd3\x8e\xdfLX\xc2\x04\xd8\xe4f\x1fA\xef\x8c\xc0S\xa2\xe2\x0c\xc3\xad\xec\x8e\x9d\xe1\x1e\xde\x83\x8a\x935\x11\x98\x0c\x97\xd9\x80\x98\xa5\x8c\xac\xb7\x99D\x82HT'\x88x\x85\x91y\x99\xc4E\xc4\x14\xba\xeb\xba\xb3\xc1"}

    @classmethod
    def setUpClass(cls):
        cls.iso = isoparser.parse(cls.ISO_FILENAME)

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
        self.recursive_test_record(self.iso.root, self.ISO_CONTENT)

        self.assertEqual(len(self.iso.root.children), 8)

if __name__ == '__main__':
        unittest.main()
