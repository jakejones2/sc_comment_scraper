from app.backend.url_input import UrlInput
import unittest


class TestUrlInput(unittest.TestCase):
    def test_add_url_file(self):
        test_url_input = UrlInput()
        test_url_input.add_url_file("test_data/test_urls.txt")
        self.assertEqual(
            test_url_input.url_list,
            [
                "https://soundcloud.com/jonimitchell/big-yellow-taxi",
                "https://soundcloud.com/herbalpert/spanish-flea",
                "https://soundcloud.com/chiarajazmyn/the-beatles-strawberry-fields-forever",
            ],
        )


if __name__ == "__main__":
    unittest.main()
