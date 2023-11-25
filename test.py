import unittest
from bs4 import BeautifulSoup
import unittest
from unittest.mock import patch
from unittest.mock import call
from job_alert import filter_jobs
"""
tests: option to mock or do live test, default mock
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
# class TestFilterJobs(unittest.TestCase):
#     @patch('os.system')
#     def test_filter_jobs(self, mock_system):
#         html = BeautifulSoup(html_doc, 'html.parser')
#         filter_jobs(html)
#
#         notification = '{base_command} -title Software Engineer -subtitle Works -message From LinkedIn -open https://www.linkedin.com/jobs/search/?currentJobId=3326240771'.format(base_command=base_command)
#         honk = 'afplay honk.aiff'
#         calls = [call(notification), call(honk)]
#         mock_system.assert_has_calls(calls, any_order=False)
#

if __name__ == '__main__':
    unittest.main()
