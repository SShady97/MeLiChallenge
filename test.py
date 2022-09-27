import unittest

from functions.date import setToLocalTime



class TestSetLocalTime(unittest.TestCase):
    def test_set_local_time(self):
        self.assertEqual(setToLocalTime("2022-09-25T03:48:51.913Z"), "2022-09-25 00:48")
        self.assertEqual(setToLocalTime("2022-03-12T05:54:22.543Z"), "2022-03-12 02:54")

if __name__ == '__main__':
    unittest.main()
