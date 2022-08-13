import unittest
import date_updater as du

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
        # no current dates
        self.assertEqual(du.split_dates(""), None)
        self.assertEqual(du.split_dates("4/8/98"), ["4/8/98"])
        self.assertEqual(du.split_dates("4/14/22, 2/7/22, 12/3/21, 12/1/21, 10/18/21"), ["4/14/22", "2/7/22", "12/3/21", "12/1/21", "10/18/21"])

    def test_num_archived_date(self):
        # no current dates
        self.assertEqual(du.split_dates("", 1), None)
        self.assertEqual(du.split_dates("4/8/98", 1), ["4/8/98"])
        self.assertEqual(du.split_dates("4/14/22, 2/7/22, 12/3/21, 12/1/21, 10/18/21", 1), ["4/14/22", "2/7/22, 12/3/21, 12/1/21, 10/18/21"])
        pass

    def test_date_regex(self):
        # no current dates
        self.assertEqual(du.split_dates(",    \n"), None)
        self.assertEqual(du.split_dates(", 4/8/98, "), ["4/8/98"])
        self.assertEqual(du.split_dates(" 4/14/22,        2/7/22,12/3/21,12/1/21,  10/18/21    \n"), ["4/14/22", "2/7/22", "12/3/21", "12/1/21", "10/18/21"])


# if module is being run directly (not imported)
if __name__ == '__main__':
    unittest.main()
