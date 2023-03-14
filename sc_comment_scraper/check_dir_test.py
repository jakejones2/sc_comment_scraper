import unittest
import check_dir

class TestCheckDir(unittest.TestCase):

    def test_check_dir(self):
        result = check_dir.check_merged_dir('tests/test_data/mock_dir')
        self.assertEqual(result, 'tests/test_data/mock_dir(1).csv')