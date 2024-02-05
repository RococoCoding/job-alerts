import re
import traceback
import json

from selenium import webdriver
from bs4 import BeautifulSoup

from database.queries.index import query_jobs_by_title_and_company, insert_job
from utils.index import JobObject, MissingValueError

driver = webdriver.Chrome()

def build_job_object(posting, site):
    job_title = posting.find('h3', class_='base-search-card__title').text.strip()
    if not job_title:
        raise MissingValueError('Missing job title')
    job_location = posting.find('span', class_='job-search-card__location').text.strip()
    company = posting.find('h4', class_='base-search-card__subtitle').text.strip()
    if not company:
        raise MissingValueError('Missing job company')
    salary_info = posting.find('span', class_='main-job-card__salary-info') or posting.find('span',
                                                                                            class_='aside-job-card__salary-info')
    if not salary_info:
        salary_info = posting.find('li', class_='job-details-jobs-unified-top-card__job-insight')
        if salary_info:
            salary_info = salary_info.text.strip()
    full_url = (posting.find('a', class_='base-card--link') or posting.find('a', class_='base-card__full-link'))['href']
    return JobObject({
        'site': site,
        'title': job_title,
        'company': company,
        'location': job_location,
        'description': '',
        'url': full_url,
        'salary': salary_info
    })


def filter_duplicates(config, job_objects):
    new_jobs = []
    for job in job_objects:
        already_seen = query_jobs_by_title_and_company(config.conn, job.title, job.company)
        print('already seen job?', bool(len(already_seen)), rf"({job.title}, {job.company})")
        if len(already_seen) == 0:
            insert_job(config.conn, job.title, job.company)
            new_jobs.append(job)
    return new_jobs


def fetch_results(url):
    print('fetch url', url)
    driver.get(url)
    source = driver.page_source
    data = re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});', source)
    data = json.loads(data[0])
    data = data["metaData"]["mosaicProviderJobCardsModel"]["results"]
    print('json data', data)
    return BeautifulSoup(driver.page_source, 'html.parser')


def get_posting(config, url, retry=False):
    driver.get(url)
    posting_response = driver.page_source
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_description = soup.find(config.description_selectors.tag, _class=config.description_selectors.class_name)
    if job_description:
        return job_description
    if not job_description and not retry:
        # print(posting_response.text)
        element = soup.find(config.description_retry_link_selectors.tag, class_=config.description_retry_link_selectors.class_name)
        if element:
            link = element['href']
            print('retry link', link)
            if link:
                return get_posting(config, link, True)
        else:
            print('cannot find retry link')
    # parse pages where the description is in a javascript object instead of html
    pattern = re.compile(r'"description":"(.*?)"employmentType"')
    match = pattern.search(posting_response.text)
    print('searching js object job description', match)
    if match:
        # Extract the desired text and replace <br> with spaces and newlines
        extracted_text = match.group(1).replace('&lt;br&gt;', ' ').replace('<br>', '\n')
        if extracted_text:
            return extracted_text
    err = MissingValueError('Missing job description')
    err.args += ('********POSTING RESPONSE*******', posting_response.text)
    print(err)


def parse_results(config, postings):
    results = []
    for posting in postings:
        try:
            job_object = build_job_object(posting, config.site)
            results.append(job_object)
        except Exception as e:
            print('error parsing posting', traceback.format_exc())
    return results

