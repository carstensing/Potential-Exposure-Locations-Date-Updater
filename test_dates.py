import unittest
import date_updater as du
from dates import Date

class TestDateUpdater(unittest.TestCase):
    # Ran before all test
    @classmethod
    def classSetUp(cls):
        pass

    # Ran after all tests
    @classmethod
    def classTearDown(cls):
        pass

    # Ran before every test
    def setUp(self):
        pass

    # Ran after every test
    def tearDown(self):
        pass

    def test_input_file_lengths(self):
        pass

    def test_num_current_dates(self):
        self.assertEqual(du.split_dates(""), None)
        self.assertEqual(du.split_dates("4/8/14"), ["4/8/14"])
        self.assertEqual(du.split_dates("4/14/22, 2/7/22, 12/3/21, 12/1/21, 10/18/21"), ["4/14/22", "2/7/22", "12/3/21", "12/1/21", "10/18/21"])

    def test_num_archived_date(self):
        self.assertEqual(du.split_dates("", 1), None)
        self.assertEqual(du.split_dates("4/8/14", 1), ["4/8/14"])
        self.assertEqual(du.split_dates("4/14/22, 2/7/22, 12/3/21, 12/1/21, 10/18/21", 1), ["4/14/22", "2/7/22, 12/3/21, 12/1/21, 10/18/21"])

    def test_date_regex(self):
        self.assertEqual(du.split_dates(",    \n"), None)
        self.assertEqual(du.split_dates(", 4/8/14, "), ["4/8/14"])
        self.assertEqual(du.split_dates(" 4/14/22,        2/7/22,12/3/21,12/1/21,  10/18/21    \n"), ["4/14/22", "2/7/22", "12/3/21", "12/1/21", "10/18/21"])

    def test_num_newer_dates(self):
        comparison_date = Date("1/2/14")
        self.assertEqual(du.num_newer_dates(["5/6/12"], comparison_date), 0)
        self.assertEqual(du.num_newer_dates(["2/7/22"], comparison_date), 1)
        self.assertEqual(du.num_newer_dates(["2/7/22", "12/3/21", "9/1/20", "5/6/12"], comparison_date), 3)

# if module is being run directly (not imported)
if __name__ == '__main__':
    unittest.main()
