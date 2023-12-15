import re

tn_base_command = base_command = '/usr/local/Cellar/terminal-notifier/2.0.0/terminal-notifier.app/Contents/MacOS/terminal-notifier'
text_spacer = '\n\n\n\n--------------------------------------------------------------------------------------------------------\n\n\n\n'

exclude_seniority = ['graduate', 'founding', 'senior', 'sr', 'director', 'staff', 'lead', 'architect', 'principal']
exclude_job_type = ['instructor', 'webmaster', 'manager', 'research', 'infrastructure', 'quality assurance', 'data scientist', 'data analytics', 'firmware', 'field services', 'systems engineer', 'sdet', 'designer', 'ux', 'ui', 'marketing', 'security', 'reliability', 'embedded', 'mobile', 'solutions engineer', 'devops', 'front end', 'front-end', 'frontend', 'seo', 'in test', 'test automation', 'QA', 'test engineer', 'manufacturing', 'electrical', 'cnc']
exclude_tech = ['oracle', 'php', 'etl', 'kubernetes', 'redis', 'sap', 'cots', 'idam', 'windows server', 'vr', 'badi', 'plc', 'powerbi', 'awd', 'flutter', 'business intelligence', 'vmware', 'blockchain', 'crypto', 'web3', 'nft', 'ai', 'aem', 'machine learning', 'ml', 'llm', 'linux', 'servicenow', 'sharepoint', 'workday', 'apigee', 'salesforce', 'shopify', 'wordpress', 'android', 'ios', 'c#', 'c\+\+', 'appian', 'aws', 'drupal', '\.net', 'dotnet', 'dot net', 'mulesoft']

# region *** search ***
inclusive_keywords = ['javascript', 'JavaScript', 'Javascript', 'JS']
exclusive_keywords = [
    '"Get It Recruit"', '"ecocareers"', '"Actalent"', 'jobot',
    '"skyrecruitment"', '"phoenix recruiting"', '"hiremefast"', '"Pattern Learning"',
    'ClearanceJobs', 'patterned learning', 'clearance', 'Tutor'
]

# Join inclusive and exclusive keywords into strings
linkedin_joined_inclusive = '%20OR%20'.join(inclusive_keywords)
linkedin_joined_exclusive = '%20OR%20'.join(exclusive_keywords)

# Final result
linkedin_keywords = f'({linkedin_joined_inclusive})%20NOT%20({linkedin_joined_exclusive})'
linkedin_base_url = 'https://www.linkedin.com'


def linkedin_search_url(time, page):
    return f'/jobs/search?keywords={linkedin_keywords}&location=United%20States&f_TPR=r{time}&f_T=9%2C25201%2C10%2C3549%2C24%2C25194&position=1&pageNum={page}'


indeed_keyword_inclusions = '+OR+'.join(inclusive_keywords)
indeed_title_exclusions = '+OR+'.join(exclude_tech) + '+OR+' + '+OR+'.join(exclude_seniority) + '+OR+' + '+OR+'.join(exclude_job_type)
# indeed_title_inclusions = '+OR+'.join()


def indeed_search_url(time, page):
    return f'/jobs?q={indeed_keyword_inclusions}+%28title%3A+engineer+OR+developer+OR+programmer+NOT+%28Senior+OR+embedded+OR+appian+OR+TS%2FSCI+OR+lead+OR+sailpoint+OR+principal+OR+devops+OR+wordpress+OR+staff+OR+sharepoint+OR+servicenow+OR+drupal+OR+Sr+OR+Sr.%29%29&l=United+States&sort=date&ts=1701278511095&pts=1701210377180&rq=1&from=HPRecent&rsIdx=0&fromage=last&newcount=267&vjk=7164afa6a7003729'
# endregion


# region *** title filter ***
all_title_exclusions = '|'.join(exclude_tech) + '|' + '|'.join(exclude_seniority) + '|' + '|'.join(exclude_job_type)
title_exclude_pattern = re.compile(rf'\b{all_title_exclusions}\b', re.IGNORECASE)

include_title = []
all_title_inclusions = '|'.join(include_title)
title_include_pattern = re.compile(rf'{all_title_inclusions}', re.IGNORECASE)

exclude_location = ['TX', 'AZ', 'GA', 'FL', 'NM', 'LA', 'AL', 'MS', 'NV', 'SC', 'AR']
all_location_exclusions = '|'.join(exclude_location)
location_exclude_pattern = re.compile(rf'^(?!.*\bremote\b)(?=.*\b(?:{all_location_exclusions})\b).*$', re.IGNORECASE)
# endregion


# region *** description filter ***
time_unit_patterns = 'year|years\'|year\'s|years|yrs|yoe|yr|y'
user_min_range = 0
user_max_range = 4
clearance_keywords = ['clearance', 'ts\/sci', 'top secret']
description_exclusion_keywords = ['web3', 'crypto', 'nft', 'cryptocurrency', 'bitcoin', 'blockchain', 'adtech', 'marketing', 'defense', 'gambling']
all_description_exclusions = "|".join(clearance_keywords) + '|' + '|'.join(description_exclusion_keywords)
print('description exclusions', all_description_exclusions)
# keyword filters
description_keyword_filter = re.compile(rf'\b{all_description_exclusions}\b', re.IGNORECASE)
# if digit + anything + time unit
experience_base_filter = re.compile(rf'(\d+).*({time_unit_patterns})', re.IGNORECASE)
# if range of digits + time unit, ex: 2-3 years, 2y-5y
experience_range_filter = re.compile(rf'(\d+)\s*(?:y)?\s*(?:-|to)\s*(\d+)\s*(?:y)?\s*(?:y)', re.IGNORECASE)
# if number+ and time unit, ex: 3+ years, 3y+, 3yoe+
experience_plus_filter = re.compile(rf'(\d+)(?:y?)\+\s*(?:y)', re.IGNORECASE)
# if minimum|min|at least + digit + time unit is mentioned, ex: minimum of 3 years experience
experience_min_filter = re.compile(rf'(\d+)\s*(?:y)', re.IGNORECASE)
# endregion

