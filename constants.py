import re
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


def linkedin_search_url(keywords, time, page):
    return f'jobs/search?keywords={keywords}&location=United%20States&f_TPR=r{time}&f_T=9%2C25201%2C10%2C3549%2C24%2C25194&position=1&pageNum={page}'
# endregion


# region *** title filter ***
exclude_seniority = ['senior', 'sr', 'director', 'staff', 'lead', 'architect', 'principal']
exclude_job_type = ['instructor', 'designer', 'ux', 'marketing', 'security', 'reliability', 'embedded', 'mobile', 'solutions engineer', 'devops', 'front end', 'frontend', 'test automation', 'QA engineer', 'test engineer', 'manufacturing', 'electrical', 'cnc']
exclude_tech = ['servicenow', 'sharepoint', 'apigee', 'salesforce', 'shopify', 'wordpress', 'android', 'ios', 'c++', 'appian', 'aws', 'drupal', '.net', 'dotnet', 'mulesoft']
all_title_exclusions = '|'.join(exclude_tech) + '|' + '|'.join(exclude_seniority) + '|' + '|'.join(exclude_job_type)
title_exclude_pattern = re.compile(r'{}'.format(all_title_exclusions), re.IGNORECASE)

include_title = ['engineer', 'developer', 'programmer']
all_title_inclusions = '|'.join(include_title)
title_include_pattern = re.compile(r'{}'.format(all_title_inclusions), re.IGNORECASE)

# endregion


# region *** description filter ***
time_unit_patterns = 'years|yrs|yoe|yr|y'
user_min_range = 0
user_max_range = 4
# if digit + anything + time unit
experience_base_filter = re.compile(rf'(\d+).*({time_unit_patterns})', re.IGNORECASE)
# if range of digits + time unit, ex: 2-3 years, 2y-5y
experience_range_filter = re.compile(rf'(\d+)\s*(?:y.*)?\s*(?:-|to)\s*(\d+)', re.IGNORECASE)
# if number+ and time unit, ex: 3+ years, 3y+, 3yoe+
experience_plus_filter = re.compile(rf'(\d+)(?:y(?:r|rs|oe)?)?\+', re.IGNORECASE)
# if minimum|min|at least + digit + time unit is mentioned, ex: minimum of 3 years experience
experience_min_filter = re.compile(rf'(?:minimum|min|at least)\s*(\d+)', re.IGNORECASE)
# endregion
