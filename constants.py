import re

tn_base_command = base_command = '/usr/local/Cellar/terminal-notifier/2.0.0/terminal-notifier.app/Contents/MacOS/terminal-notifier'

# region *** search ***
inclusive_keywords = ['javascript', 'JavaScript', 'Javascript', 'JS']
exclusive_keywords = [
    '"Get It Recruit"', '"ecocareers"', '"Actalent"', 'jobot',
    '"skyrecruitment"', '"phoenix recruiting"', '"hiremefast"', '"Pattern Learning"',
    'ClearanceJobs', 'patterened', 'clearance', 'Tutor'
]
# Join inclusive and exclusive keywords into strings
joined_inclusive = '%20OR%20'.join(inclusive_keywords)
joined_exclusive = '%20OR%20'.join(exclusive_keywords)

# Final result
linkedin_keywords = f'({joined_inclusive})%20NOT%20({joined_exclusive})'
linkedin_base_url = 'https://www.linkedin.com'


def linkedin_search_url(time, page):
    return f'/jobs/search?keywords={linkedin_keywords}&location=United%20States&f_TPR=r{time}&f_T=9%2C25201%2C10%2C3549%2C24%2C25194&position=1&pageNum={page}'
# endregion


# region *** title filter ***
exclude_seniority = ['graduate', 'senior', 'sr', 'director', 'staff', 'lead', 'architect', 'principal']
exclude_job_type = ['instructor', 'systems engineer', 'sdet', 'designer', 'ux', 'ui', 'marketing', 'security', 'reliability', 'embedded', 'mobile', 'solutions engineer', 'devops', 'front end', 'front-end', 'frontend', 'seo', 'in test', 'test automation', 'QA', 'test engineer', 'manufacturing', 'electrical', 'cnc']
exclude_tech = ['oracle', 'vmware', 'ai', 'aem', 'llm', 'linux', 'servicenow', 'sharepoint', 'apigee', 'salesforce', 'shopify', 'wordpress', 'android', 'ios', 'c++', 'appian', 'aws', 'drupal', '.net', 'dotnet', 'dot net', 'mulesoft']
all_title_exclusions = '|'.join(exclude_tech) + '|' + '|'.join(exclude_seniority) + '|' + '|'.join(exclude_job_type)
title_exclude_pattern = re.compile(rf'\b{all_title_exclusions}\b', re.IGNORECASE)

include_title = ['engineer', 'developer', 'programmer']
all_title_inclusions = '|'.join(include_title)
title_include_pattern = re.compile(rf'{all_title_inclusions}', re.IGNORECASE)

exclude_location = ['TX', 'AZ', 'GA', 'FL', 'NM', 'LA', 'AL', 'MS', 'NV', 'SC', 'AR']
all_location_exclusions = '|'.join(exclude_location)
location_exclude_pattern = re.compile(rf'^(?!.*\bremote\b)(?=.*\b(?:{all_location_exclusions})\b).*$', re.IGNORECASE)
# endregion


# region *** description filter ***
time_unit_patterns = 'years|yrs|yoe|yr|y'
user_min_range = 0
user_max_range = 4
# clearance filters
clearance_filter = re.compile("|".join(['clearance', 'ts/sci', 'top secret']), re.IGNORECASE)
# if digit + anything + time unit
experience_base_filter = re.compile(rf'(\d+).*({time_unit_patterns})', re.IGNORECASE)
# if range of digits + time unit, ex: 2-3 years, 2y-5y
experience_range_filter = re.compile(rf'(\d+)\s*(?:y.*)?\s*(?:-|to)\s*(\d+)', re.IGNORECASE)
# if number+ and time unit, ex: 3+ years, 3y+, 3yoe+
experience_plus_filter = re.compile(rf'(\d+)(?:y(?:r|rs|oe)?)?\+', re.IGNORECASE)
# if minimum|min|at least + digit + time unit is mentioned, ex: minimum of 3 years experience
experience_min_filter = re.compile(rf'(?:minimum|min|at least)\s*(\d+)', re.IGNORECASE)
# endregion
