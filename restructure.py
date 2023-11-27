import sys
import requests
from bs4 import BeautifulSoup
import os
import re
from constants import linkedin_base_url, linkedin_search_url, title_include_pattern, title_exclude_pattern, \
    experience_base_filter, experience_range_filter, user_min_range, user_max_range, experience_plus_filter, \
    experience_min_filter

timing = sys.argv[0]
#region *** site config definitions ***
supported_sites = {
    'linkedin': {
        'base_url': linkedin_base_url,
        'search_url': f'{linkedin_base_url}{linkedin_search_url}'
    },
    # 'indeed': {
    #     'base_url': 'https://www.indeed.com',
    # }
}

class SiteConfig:
    def __init__(self, site):
        self.site = site
        self._base_url = self.get_base_url()

    def get_base_url(self):
        if not self.site in supported_sites:
            raise Exception('Site not supported')
        return self.supported_sites[self.site]['base_url']

    @property
    def base_url(self):
        return self._base_url

#endregion *** ****

#region *** function definitions ***
# queries site and parses result to return only the preview cards
def search_site(config):
    linkedin_search_response = requests.get(config.search_url)
    soup = BeautifulSoup(linkedin_search_response.text, 'html.parser')
    list_with_class_test = soup.find('ul', class_='jobs-search__results-list')
    return list_with_class_test.find_all('li')


def create_notification() -> notification_obj:

# compares job title to regex filter of required inclusive keywords and exclusive keywords
def title_passes_filter(card):
    job_title = card.find('h3', class_='base-search-card__title').text.strip()
    return True if title_include_pattern and not title_exclude_pattern.search(job_title) else False

def get_posting(url):
    posting_response = requests.get(url)
    soup = BeautifulSoup(posting_response.text, 'html.parser')
    job_description = soup.find('div', class_='show-more-less-html__markup')
    return job_description

def description_passes_filter(job_description):
    list_items = job_description.find_all('li')
    if not list_items:
        list_items = job_description.text()
    for item in list_items:
        item_text = item.text()
        # If the job description does not mention specific year(s) of experience, it passes the filter
        if not experience_base_filter.search(item_text):
            return True
        # if job description mentions a range, check if the range overlaps with user input range
        range_matches = re.findall(experience_range_filter, item_text)
        # TODO: if len greater than 2, log error
        if len(range_matches):
            [posting_min, posting_max] = [int(number) for number in range_matches]
            if any(num in range(user_min_range, user_max_range + 1) for num in range(posting_min, posting_max + 1)):
                return True
        # if the job mentions num+ years of experience, check if the num is less than the user's max
        plus_matches = re.findall(experience_plus_filter, item_text)
        # TODO: if len greater than 1, log error
        if len(plus_matches):
            if plus_matches[0] <= user_max_range:
                return True
        # if the job mentions at least/min years of experience
        minimum_matches = re.findall(experience_min_filter, item_text)
        if len(minimum_matches):
            if minimum_matches[0] <= user_max_range:
                return True

def push_notification():


def play_alert():
    # HONK

def save_notifications:


def get_notifications:
    all_notifications = []
    for site in supported_sites:
        config = SiteConfig(site)

        preview_cards = search_site(config)

        site_notifications = filter_response(config, preview_cards)
        all_notifications = all_notifications + site_notifications
    return all_notifications


def filter_response(config, preview_cards):
    notifications = []
    for card in preview_cards:
        if title_passes_filter(card):
            full_url = (card.find('a', class_='base-card--link'))['href']
            # if it passes title filter, get posting for full job description
            job_description = get_posting(full_url)

            if description_passes_filter(job_description):
                # if it passes body filter, create a notification object
                notifications.append(create_notification(tbd_input))
    return notifications

def find_notifications():
    all_notifications = get_notifications()

    # archive notifications to a text file
    save_notifications(all_notifications)

    # individual notifications for small batches
    if len(all_notifications) < 5:
        for notification in all_notifications:
            push_notification(notification)
    else:
        # for larger batches, create a single notification that opens the saved notifications file
        push_notification(create_notification(tbd_input))
    play_alert()
#endregion

# run script
find_notifications()
