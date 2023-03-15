import unittest
from app.backend import check_dir

class TestFilter:
     
     filtername = 'NE, NT, '


class TestCheckDir(unittest.TestCase):

    def test_check_merged_dir(self):
        result = check_dir.check_merged_dir('test_data/mock_dir')
        self.assertEqual(result, 'test_data/mock_dir(1).csv')

    def test_check_ind_dir(self):
        result = check_dir.check_ind_dir('test_data/mock_dir', TestFilter)
        self.assertEqual(result, 'test_data/mock_dir[filters = NE, NT](1).csv')


if __name__ == '__main__':
    unittest.main()