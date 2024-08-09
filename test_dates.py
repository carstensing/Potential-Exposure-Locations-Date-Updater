import unittest
import date_updater as du
from date import Date

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

    def test_get_num_lines(self):
        # TODO
        pass

    def test_num_current_dates(self):
        self.assertEqual(du.split_dates(""), [])
        self.assertEqual(du.split_dates("4/8/14"), ["4/8/14"])
        self.assertEqual(du.split_dates("4/14/22, 2/7/22, 12/3/21, 12/1/21, 10/18/21"), ["4/14/22", "2/7/22", "12/3/21", "12/1/21", "10/18/21"])

    def test_num_archived_date(self):
        self.assertEqual(du.split_dates("", 1), [])
        self.assertEqual(du.split_dates("4/8/14", 1), ["4/8/14"])
        self.assertEqual(du.split_dates("4/14/22, 2/7/22, 12/3/21, 12/1/21, 10/18/21", 1), ["4/14/22", "2/7/22, 12/3/21, 12/1/21, 10/18/21"])

    def test_date_regex(self):
        self.assertEqual(du.split_dates(",    \n"), [])
        self.assertEqual(du.split_dates(", 4/8/14, "), ["4/8/14"])
        self.assertEqual(du.split_dates(" 4/14/22,        2/7/22,12/3/21,12/1/21,  10/18/21    \n"), ["4/14/22", "2/7/22", "12/3/21", "12/1/21", "10/18/21"])

    def test_num_newer_dates(self):
        comparison_date = Date("1/2/14")
        self.assertEqual(du.num_newer_dates(["5/6/12"], comparison_date), 0)
        self.assertEqual(du.num_newer_dates(["2/7/22"], comparison_date), 1)
        self.assertEqual(du.num_newer_dates(["2/7/22", "12/3/21", "9/1/20", "5/6/12"], comparison_date), 3)

    def test_get_cur_output_string_and_invalid_dates(self):
        dates_line = "4/14/22, 2/7/22, 12/3/21, 12/1/21, 10/18/21\n"
        dates_list = ["4/14/22", "2/7/22", "12/3/21", "12/1/21", "10/18/21"]
        self.assertEqual(du.get_cur_output_string_and_invalid_dates(dates_line, Date("5/1/22")), ("\n", dates_list))
        self.assertEqual(du.get_cur_output_string_and_invalid_dates(dates_line, Date("3/4/22")), ("4/14/22\n", dates_list[1:]))
        self.assertEqual(du.get_cur_output_string_and_invalid_dates(dates_line, Date("12/2/21")), ("4/14/22, 2/7/22, 12/3/21\n", dates_list[3:]))
        self.assertEqual(du.get_cur_output_string_and_invalid_dates(dates_line, Date("4/1/14")), (dates_line, []))
        self.assertEqual(du.get_cur_output_string_and_invalid_dates("", Date("4/1/14")), ("\n", []))

    def test_get_arc_output_string(self):
        invalid_dates_line = "4/14/22, 2/7/22, 12/3/21, 12/1/21, 10/18/21\n"
        invalid_dates = ["4/14/22", "2/7/22", "12/3/21", "12/1/21", "10/18/21"]
        self.assertEqual(du.get_arc_output_string("\n", invalid_dates), invalid_dates_line)
        self.assertEqual(du.get_arc_output_string("3/8/16\n", invalid_dates), "4/14/22, 2/7/22, 12/3/21, 12/1/21, 10/18/21, 3/8/16\n")
        self.assertEqual(du.get_arc_output_string("3/8/16, text\n", invalid_dates), "4/14/22, 2/7/22, 12/3/21, 12/1/21, 10/18/21, 3/8/16, text\n")
        self.assertEqual(du.get_arc_output_string("4/15/22\n", invalid_dates), "4/15/22\n")
        self.assertEqual(du.get_arc_output_string("10/18/21, 3/8/16\n", invalid_dates), "4/14/22, 2/7/22, 12/3/21, 12/1/21, 10/18/21, 3/8/16\n")
        self.assertEqual(du.get_arc_output_string("\n", []), "\n")
        self.assertEqual(du.get_arc_output_string(invalid_dates_line, []), invalid_dates_line)

# if module is being run directly (not imported)
if __name__ == "__main__":
    unittest.main()
