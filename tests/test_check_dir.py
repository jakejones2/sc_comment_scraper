import unittest
from app.backend import check_dir

class TestFilter:
     
     filtername = 'NE, NT, '


class TestCheckDir(unittest.TestCase):

    def test_check_ind_dir(self):
        result = check_dir.create_ind_dir('tests/test_data/mock_dir', TestFilter)
        self.assertEqual(result, 'tests/test_data/mock_dir[filters = NE, NT](1).csv')

    def test_check_merged_dir(self):
        result = check_dir.create_merged_dir('tests/test_data/mock_dir')
        self.assertEqual(result, 'tests/test_data/mock_dir(1).csv')


'''https://docs.pytest.org/en/6.2.x/fixture.html'''
# I broke these tests. Anyway - should use pytest! 
# Can we create various edge case fixtures for input to the GUI?
# Rather than this class TestFilter etc. Otherwise will be lots of repeats.
# Also, check the new scraper works! Moved stuff to check_dir. 
# Can we refactor check_dir before it's too late? could call csv_path.
# in this case, don't forget the test_data folder and its contents.

if __name__ == '__main__':
    unittest.main()