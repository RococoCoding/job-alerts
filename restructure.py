import sys
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
import re
import subprocess
import traceback

from constants import linkedin_base_url, linkedin_search_url, title_include_pattern, title_exclude_pattern, \
    experience_base_filter, experience_range_filter, user_min_range, user_max_range, experience_plus_filter, \
    experience_min_filter, clearance_filter, location_exclude_pattern, tn_base_command, text_spacer


class MissingValueError(Exception):
    def __init__(self, message="Could not find value"):
        self.message = message


today_date = datetime.now()
formatted_date = today_date.strftime('%Y_%m_%d')
formatted_datetime = today_date.strftime("%B %d, %Y %I:%M %p")
timing = sys.argv[1]
log_file_name = f'logs/errors_{today_date.strftime("%Y_%m_%d-%Y_%p_%I:%M")}.txt'
errors = []
base_directory = '/Users/alicechang/Projects/job-alerts/'


# region *** site config definitions ***
supported_sites = {
    'linkedin': {
        'base_url': linkedin_base_url,
        'search_url': f'{linkedin_base_url}{linkedin_search_url(timing, 0)}'
    },
    # 'indeed': {
    #     'base_url': 'https://www.indeed.com',
    # }
}


class SiteConfig:
    def __init__(self, site):
        self.site = site
        self._base_url = self.get_base_url()
        self._search_url = self.get_search_url()

    def get_base_url(self):
        if self.site not in supported_sites:
            raise Exception('Site not supported')
        return supported_sites[self.site]['base_url']

    def get_search_url(self):
        if self.site not in supported_sites:
            raise Exception('Site not supported')
        print('search url: ', supported_sites[self.site]['search_url'])
        return supported_sites[self.site]['search_url']

    @property
    def base_url(self):
        return self._base_url

    @property
    def search_url(self):
        return self._search_url

# endregion


# region *** function definitions ***
# queries site and parses result to return only the preview cards
def search_site(config):
    all_results = []
    start = 0
    uri_set = set()
    count = 0

    while count < 5:
        count = 0
        # search site
        print('searching site', config.search_url, start)
        linkedin_search_response = requests.get(f'{config.search_url}&start={start}')
        soup = BeautifulSoup(linkedin_search_response.text, 'html.parser')
        # push results to return list
        results_list = soup.find('ul', class_='jobs-search__results-list')
        if not results_list:
            print('missing results list', soup)
            count += 1
            continue
        list_items = results_list.find_all('li')
        if len(list_items):
            for item in list_items:
                try:
                    urn = (item.find('div', class_='base-card') or item.find('a', class_='base-card'))['data-entity-urn']
                    if urn:
                        [_, _, _, uri] = urn.split(':')
                        if uri in uri_set:
                            count += 1
                        else:
                            uri_set.add(uri)
                            all_results.append(item)
                except Exception as e:
                    e.args += ('urn element', item)
                    errors.append(traceback.format_exc())
            start += len(all_results)
        else:
            print('no list item length')
            count += 1
    return all_results


# compares job title to regex filter of required inclusive keywords and exclusive keywords
def title_passes_filter(job_title):
    return True if title_include_pattern.search(job_title) and not title_exclude_pattern.search(job_title) else False


def location_passes_filter(job_location):
    return True if not location_exclude_pattern.search(job_location) else False


def get_posting(url):
    posting_response = requests.get(url)
    soup = BeautifulSoup(posting_response.text, 'html.parser')
    job_description = soup.find('div', class_='show-more-less-html__markup')
    if not job_description:
        err = MissingValueError('Missing job description')
        err.args += ('********POSTING RESPONSE*******', posting_response.text)
        print(err)
    return job_description


def description_passes_filter(job_description):
    item_text = job_description.get_text(' ')
    print(item_text)
    # if job description mentions security clearance, fails filter
    if re.search(clearance_filter, item_text):
        return False
    # if job description mentions a range, check if the range overlaps with user input range
    range_matches = re.findall(experience_range_filter, item_text)
    for range_match in range_matches:
        [posting_min, posting_max] = [int(number) for number in range_match]
        print('posting min-max', range_matches, posting_min, posting_max)
        if not any(num in range(user_min_range, user_max_range + 1) for num in range(posting_min, posting_max + 1)):
            print('failed min-max')
            return False
    # if the job mentions num+ years of experience, check if the num is less than the user's max
    plus_matches = re.findall(experience_plus_filter, item_text)
    print('posting with plus', plus_matches)
    for plus_match in plus_matches:
        if int(plus_match) > user_max_range:
            print('failed plus')
            return False
    # if the job mentions at least/min years of experience
    minimum_matches = re.findall(experience_min_filter, item_text)
    print('posting with min', minimum_matches)
    # if more than one, pass filter so we can manually review and figure out what to do with them
    for minimum_match in minimum_matches:
        if int(minimum_match) > user_max_range:
            print('failed min')
            return False
    return True


def create_notification_command(job_info):
    title = f"-title '{job_info['title']}'"
    subtitle = f"-subtitle '{job_info['company']}'"
    url = f"-open {job_info['url']}"
    message = f"-message 'from {job_info['site']}'"
    return f'{tn_base_command} {title} {subtitle} {message} {url}'


def push_notification(command):
    os.system(command)


def play_alert():
    os.system('afplay /Users/alicechang/Projects/job-alerts/honk.aiff')


def format_job_description(soup):
    formatted_text = ''
    for element in soup:
        if element.name == 'ul':
            formatted_text += '\n'
            for li in element.find_all('li'):
                formatted_text += f"  • {li.get_text(strip=True)}\n"
        else:
            formatted_text += f"{element.get_text(strip=True)}\n"
    return formatted_text


def archive_jobs(jobs):
    archive_text = f'{formatted_datetime} ({len(jobs)} results found)'
    for j in jobs:
        job_text = f"\n\n\nTitle: {j['title']}\nCompany: {j['company']}\nLocation: {j['location']}\nSalary: {j['salary']}" \
            f"\nLink: {j['url']}\nJob Description: {format_job_description(j['description'])}"
        archive_text = archive_text + job_text

    # one file per day
    file_name = f'job_archives/job_postings_{formatted_date}.txt'

    # append if file already exists
    if os.path.exists(f'{base_directory}{file_name}'):
        with open(f'{base_directory}{file_name}', 'r') as file:
            existing_content = file.read()

        # Combine the new text with the existing content
        updated_content = archive_text + text_spacer + existing_content

        # Write the updated content back to the file
        with open(f'{base_directory}{file_name}', 'w') as file:
            file.write(updated_content)
    else:
        # Open the file in 'w' mode (write mode) if it doesn't exist
        with open(f'{base_directory}{file_name}', 'w') as file:
            file.write(archive_text)
    return f'/Users/alicechang/Projects/job-alerts/{file_name}'


def filter_response(config, preview_cards):
    approved_jobs = []
    for card in preview_cards:
        try:
            job_title = card.find('h3', class_='base-search-card__title').text.strip()
            if not job_title:
                raise MissingValueError('Missing job title')
            job_location = card.find('span', class_='job-search-card__location').text.strip()
            print('\n*********', job_title, job_location)
            if title_passes_filter(job_title) and location_passes_filter(job_location):
                full_url = (card.find('a', class_='base-card--link') or card.find('a', class_='base-card__full-link'))['href']
                # if it passes title filter, get posting for full job description
                job_description = get_posting(full_url)
                try:
                    if description_passes_filter(job_description):
                        salary_info = card.find('span', class_='main-job-card__salary-info') or card.find('span', class_='aside-job-card__salary-info')
                        company = card.find('h4', class_='base-search-card__subtitle').text.strip()
                        job_object = {
                            'site': config.site,
                            'title': job_title,
                            'company': company,
                            'description': job_description,
                            'location': job_location,
                            'url': full_url,
                            'salary': salary_info
                        }
                        approved_jobs.append(job_object)
                except Exception as e:
                    e.args += ('\n\n*****EXCEPTED DESCRIPTION******', job_description)
                    raise
            else:
                print('failed title filter: ', title_passes_filter(job_title), location_passes_filter(job_location))
        except Exception as e:
            e.args += ('\n\n*****EXCEPTED CARD*******', card)
            errors.append(traceback.format_exc())
    return approved_jobs


def find_jobs():
    combined_approved_jobs = []
    for site in supported_sites:
        try:
            config = SiteConfig(site)

            preview_cards = search_site(config)

            site_jobs = filter_response(config, preview_cards)
            combined_approved_jobs = combined_approved_jobs + site_jobs
        except Exception as e:
            errors.append(traceback.format_exc())
    return combined_approved_jobs
# endregion


# run script
try:
    filtered_jobs = find_jobs()

    # individual notifications for small batches
    if len(filtered_jobs):
        # archive notifications to a text file
        archive_file_path = archive_jobs(filtered_jobs)

        # notify individually for smaller batches
        if len(filtered_jobs) < 5:
            for job in filtered_jobs:
                push_notification(create_notification_command(job))
        # or for larger batches, open the saved archive
        else:
            subprocess.run(['/usr/local/bin/code', archive_file_path])
        play_alert()
    if len(errors):
        # log errors to a file for review
        with open(f'{base_directory}{log_file_name}', 'w') as file:
            file.write(f'{len(errors)} errors\n\n{errors}')
        subprocess.run(['open', '-t', f'/Users/alicechang/Projects/job-alerts/{log_file_name}'])
        play_alert()
except Exception as e:
    # log errors to a file for review
    with open(f'{base_directory}{log_file_name}', 'w') as file:
        file.write(traceback.format_exc())
    subprocess.run(['open',  '-t', f'/Users/alicechang/Projects/job-alerts/{log_file_name}'])
    play_alert()


