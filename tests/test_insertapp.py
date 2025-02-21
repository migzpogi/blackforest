import unittest
from InsertApp import foo


class TestInsertApp(unittest.TestCase):

    def test_scrape_stub(self):
        self.assertEqual(foo(), 1)


if __name__ == '__main__':
    unittest.main()