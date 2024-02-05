from constants import title_exclude_pattern, location_exclude_pattern, experience_range_filter, \
    user_min_range, user_max_range, experience_plus_filter, experience_min_filter, description_keyword_filter
import re
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")


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


def title_passes_filter(job_title):
    return True if not title_exclude_pattern.search(job_title) else False


def location_passes_filter(job_location):
    return True if not location_exclude_pattern.search(job_location) else False


def description_passes_filter(job_description):
    if not isinstance(job_description, str):
        soup_text = job_description.get_text(' ')
        item_text = format_job_description(soup_text)
    else:
        item_text = job_description
    if description_keyword_filter.search(item_text):
        print('failed description keyword filter: ', description_keyword_filter.search(item_text))
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

    # calculate num of tokens for jobs that pass
    num_tokens = len(encoding.encode(item_text))
    print(num_tokens, item_text)
    return True
