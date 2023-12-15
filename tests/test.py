import unittest
from bs4 import BeautifulSoup
import unittest
from unittest.mock import patch
from unittest.mock import call
from job_alert import filter_jobs

"""
tests: option to mock, default mock
- SiteConfig returns the correct config
- SiteConfig throws error if no config
- search site requests.get is called with correct input
    - returns parsed soup
- filter_title excludes entries with excluded words even if includes words in inclusion filter
    -returns only entries with words in inclusion filter
- get_posting is called with correct input
    - returns parsed soup
- filter_description excludes entries with excluded words
- create_notification returns a valid notification object
- filter_response + get_notifications returns an array of notification objects
    - if error in cards/sites loop, skips that card/site and logs error
- save_notifications creates a text file containing notifications archive
    - does nothing if no notifications
- push_notification calls terminal-notifier with the correct input
- find_notifications
    - if test data len is less than 5, calls push_notification len times with correct input
    - if test dtaa len is >= 5, calls push_notification once with correct input
    - always plays alert exactly once
"""
from job_alert import SiteConfig, search_site, get_posting, filter_response, push_notification


class TestSiteConfig(unittest.TestCase):
    def test_returns_correct_config(self):
        linkedin_config = SiteConfig('linkedin')
        self.assertEqual(linkedin_config.base_url, 'http://www.linkedin.com')

        # indeed_config = SiteConfig('indeed')
        # self.assertEqual(indeed_config.base_url, 'http://www.indeed.com')

    def test_throws_error_if_no_config(self):
        with self.assertRaises(Exception) as context:
            SiteConfig('unsupported_site')

        self.assertTrue('Site not supported' in str(context.exception))


class TestSearchSite(unittest.TestCase):
    def test_requests_get_is_called_with_correct_input(self):
        pass


class TestFilterTitle(unittest.TestCase):
    def test_excludes_entries_with_excluded_words(self):
        pass


class TestGetPosting(unittest.TestCase):
    def test_is_called_with_correct_input(self):
        pass


class TestFilterDescription(unittest.TestCase):
    def test_excludes_entries_with_excluded_words(self):
        pass


class TestCreateNotification(unittest.TestCase):
    def test_returns_valid_notification_object(self):
        pass


class TestFilterResponse(unittest.TestCase):
    def test_get_notifications_returns_array_of_notification_objects(self):
        pass


class TestSaveNotifications(unittest.TestCase):
    def test_creates_text_file(self):
        pass


class TestPushNotification(unittest.TestCase):
    def test_calls_terminal_notifier_with_correct_input(self):
        pass


class TestFindNotifications(unittest.TestCase):
    def test_find_notifications(self):
        pass


if __name__ == '__main__':
    unittest.main()
