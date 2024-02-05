import time
from datetime import datetime
import os
import sqlite3
import subprocess
import sys
import traceback

from constants import linkedin_base_url, linkedin_query, tn_base_command, text_spacer, indeed_base_url, \
    indeed_query
from fetch.index import get_posting, fetch_results, parse_results, filter_duplicates
from filter.index import description_passes_filter, title_passes_filter, location_passes_filter

today_date = datetime.now()
formatted_date = today_date.strftime('%Y_%m_%d')
formatted_datetime = today_date.strftime("%B %d, %Y %I:%M %p")
timing = sys.argv[1]
log_file_name = f'logs/errors_{today_date.strftime("%Y_%m_%d-%Y_%p_%I:%M")}.txt'
errors = []
base_directory = '/Users/alicechang/Projects/job-alerts/'


class Selectors:
    def __init__(self, tag, class_name):
        self.tag = tag
        self.class_name = class_name


# region *** site config definitions ***
supported_sites = {
    'linkedin': {
        'base_url': linkedin_base_url,
        'search_url': f'{linkedin_base_url}{linkedin_query(timing, 0)}',
        'results_selectors': Selectors('ul', 'jobs-search__results-list'),
        'description_selectors': Selectors('div', 'show-more-less-html__markup'),
        'description_retry_link_selectors': Selectors('a', 'base-card__full-link')
    },
    # 'indeed': {
    #     'base_url': indeed_base_url,
    #     'search_url': f'{indeed_base_url}{indeed_query(0)}',
    #     'results_selectors': Selectors('ul', 'css-zu9cdh eu4oa1w0'),
    #     'description_selectors': Selectors('div', 'show-more-less-html__markup'),
    #     'description_retry_link_selectors': Selectors('a', 'base-card__full-link')
    # }
}


class SiteConfig:
    def __init__(self, site, conn):
        self.conn = conn
        self.site = site
        self._base_url = self.get_base_url()
        self._search_url = self.get_search_url()
        self._results_selectors = self.get_results_selectors()
        self._description_selectors = self.get_description_selectors()
        self._description_retry_link_selectors = self.get_description_retry_link_selectors()

    def get_base_url(self):
        if self.site not in supported_sites:
            raise Exception('Site not supported', self.site)
        return supported_sites[self.site]['base_url']

    def get_search_url(self):
        if self.site not in supported_sites:
            raise Exception('Site not supported', self.site)
        return supported_sites[self.site]['search_url']

    def get_results_selectors(self):
        if self.site not in supported_sites:
            raise Exception('Site not supported', self.site)
        return supported_sites[self.site]['results_selectors']

    def get_description_selectors(self):
        if self.site not in supported_sites:
            raise Exception('Site not supported', self.site)
        return supported_sites[self.site]['description_selectors']

    def get_description_retry_link_selectors(self):
        if self.site not in supported_sites:
            raise Exception('Site not supported', self.site)
        return supported_sites[self.site]['description_retry_link_selectors']

    @property
    def base_url(self):
        return self._base_url

    @property
    def search_url(self):
        return self._search_url

    @property
    def results_selectors(self):
        return self._results_selectors

    @property
    def description_selectors(self):
        return self._description_selectors

    @property
    def description_retry_link_selectors(self):
        return self._description_retry_link_selectors
# endregion


# region *** function definitions ***
def create_notification_command(job_info):
    title = f"-title '{job_info.title}'"
    subtitle = f"-subtitle '{job_info.company}'"
    url = f"-open {job_info.url}"
    message = f"-message 'from {job_info.site}'"
    return f'{tn_base_command} {title} {subtitle} {message} {url}'


def push_notification(command):
    os.system(command)


def play_alert():
    os.system(f'afplay {base_directory}assets/honk_glass.aiff')


def archive_jobs(jobs):
    archive_text = f'{formatted_datetime} ({len(jobs)} results found)'
    for j in jobs:
        job_text = f"\n\n\nTitle: {j.title}\nCompany: {j.company}\nLocation: {j.location}\nSalary: {j.salary}" \
            f"\nLink: {j.url}\nJob Description: {j.description}"
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
    return f'{base_directory}{file_name}'


def filter_response(config, jobs):
    approved_jobs = []
    for job in jobs:
        try:
            print('\n*********', job.title, job.location)
            if title_passes_filter(job.title) and location_passes_filter(job.location):
                # if it passes title & location filter, get posting for full job description
                job_description = get_posting(config, job.url)
                if job_description:
                    try:
                        if description_passes_filter(job_description):
                            job.description = job_description
                            approved_jobs.append(job)
                    except Exception as e:
                        e.args += ('\n\n*****EXCEPTED DESCRIPTION******', job_description)
                        raise
            else:
                print('failed title/location filter: ', title_passes_filter(job.title), location_passes_filter(job.location))
        except Exception as e:
            e.args += ('\n\n*****EXCEPTED CARD*******', job)
            errors.append(traceback.format_exc())
    return approved_jobs


def search_site(config, retry=0):
    all_results = []
    total_results = 0
    duplicate_count = 0

    # query site
    print('searching linkedin', config.search_url, total_results)
    while duplicate_count < 10:
        # fetch results
        soup = fetch_results(f'{config.search_url}&start={total_results}')
        results_list = soup.find(config.results_selectors.tag, class_=config.results_selectors.class_name)
        # print('results list: ', soup)
        if not results_list:
            if retry <= 3:
                # wait 3 seconds and retry fetch
                time.sleep(3)
                return search_site(config, 1)
            else:
                e.args += ('\n\n*****NO RESULTS FOUND*******', soup)
                errors.append(traceback.format_exc())
                return all_results

        # process postings
        list_items = results_list.find_all('li')
        if list_items and len(list_items):
            total_results += len(list_items)
            parsed_results = parse_results(config, list_items)
            new_jobs = filter_duplicates(config, parsed_results)
            all_results = all_results + new_jobs
            duplicate_count = len(list_items) - len(new_jobs)
            print('duplicate count', duplicate_count)
        else:
            e.args += ('\n\n*****Could not find list items*******', results_list)
            errors.append(traceback.format_exc())
    return all_results

# endregion


# run script
try:
    db_connection = sqlite3.connect(f'{base_directory}database/jobs.db')
    all_filtered_jobs = []
    for supported_site in supported_sites:
        try:
            site_config = SiteConfig(supported_site, db_connection)
            all_jobs = search_site(site_config)
            filtered_jobs = filter_response(site_config, all_jobs)
            all_filtered_jobs = all_filtered_jobs + filtered_jobs
        except Exception as e:
            errors.append(traceback.format_exc())

    len_all_filtered_jobs = len(all_filtered_jobs)

    if len_all_filtered_jobs:
        # archive notifications to a text file
        archive_file_path = archive_jobs(all_filtered_jobs)

        # if small batch, notify individually
        if len_all_filtered_jobs < 5:
            for filtered_job in all_filtered_jobs:
                push_notification(create_notification_command(filtered_job))
        # if larger batch, open the saved archive
        else:
            subprocess.run(['/usr/local/bin/code', archive_file_path])
        play_alert()

    if len(errors):
        # log errors to a file for review
        with open(f'{base_directory}{log_file_name}', 'w') as file:
            file.write(f'{len(errors)} errors\n\n{errors}')
        subprocess.run(['open', '-t', f'{base_directory}{log_file_name}'])
        play_alert()

    db_connection.close()
except Exception as e:
    # log errors to a file for review
    with open(f'{base_directory}{log_file_name}', 'w') as file:
        file.write(traceback.format_exc())
    subprocess.run(['open',  '-t', f'{base_directory}{log_file_name}'])
    play_alert()


