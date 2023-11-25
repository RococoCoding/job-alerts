import requests
from bs4 import BeautifulSoup
import os
import re

# query postings in the last 20 min (in seconds)
time = 1200

# use linkedin filters to avoid spammy sites
keywords = '(javascript%20OR%20JavaScript%20OR%20Javascript%20OR%20JS)%20NOT%20("Get%20It%20Recruit"%20OR%20"ecocareers"%20OR%20"Actalent"%20OR%20jobot%20OR%20"skyrecruitment"%20OR%20"phoenix%20recruiting"%20OR%20"hiremefast"%20OR%20"Pattern%20Learning"%20OR%20ClearanceJobs%20OR%20patterened%20OR%20clearance%20OR%20Tutor)'
linked_in_url = 'https://www.linkedin.com/jobs/search?keywords={keywords}&location=United%20States&f_TPR=r{time}&f_T=9%2C25201%2C10%2C3549%2C24%2C25194&position=1&pageNum=0'.format(keywords=keywords, time=time)
li_search_response = requests.get(linked_in_url)
print(linked_in_url)
# Parse the results using BeautifulSoup
soup = BeautifulSoup(li_search_response.text, 'html.parser')

# setup command to run terminal-notifier
base_command = '/usr/local/Cellar/terminal-notifier/2.0.0/terminal-notifier.app/Contents/MacOS/terminal-notifier'
base_url_job_link = 'https://www.linkedin.com/jobs/search/?currentJobId='

# static fields for terminal-notifier
message = '-message "From LinkedIn"'
app_icon = '-appIcon https://raw.githubusercontent.com/RococoCoding/job-alerts/main/honk.png'


def filter_jobs(html):
    # Extract the information you need (this depends on the structure of the website)
    # For example, to get the text of the first paragraph:
    # Find the list with class "test"
    list_with_class_test = html.find('ul', class_='jobs-search__results-list')

    # Find all list items inside the list
    list_items = list_with_class_test.find_all('li')
    # set up keyword exclusions list for job titles
    exclude_seniority = 'senior|sr|director|staff|lead|architect|principal'
    exclude_job_type = 'instructor|designer|ux|marketing|security|reliability|embedded|mobile|solutions engineer|devops|front end|frontend|test automation|QA engineer|test engineer|manufacturing|electrical|cnc'
    exclude_tech = 'servicenow|sharepoint|apigee|salesforce|shopify|wordpress|android|ios|c\+\+|appian|aws|drupal|\.net|dotnet|mulesoft'
    all_exclusions = exclude_tech + '|' + exclude_seniority + '|' + exclude_job_type
    title_exclude_pattern = re.compile(r'{}'.format(all_exclusions), re.IGNORECASE)

    include_title = 'engineer|developer|programmer'
    title_include_pattern = re.compile(r'{}'.format(include_title), re.IGNORECASE)

    play_sound = False
    # Now 'list_items' is a list of all 'li' tags inside the 'ul' with class "test"
    for li in list_items:
        # Get job title
        job_title = li.find('h3', class_='base-search-card__title').text.strip()
        company = li.find('h4', class_='base-search-card__subtitle').text.strip()

        # Exclude listings with 'Senior' in the title
        if title_include_pattern and not title_exclude_pattern.search(job_title):
            # Get the link to the job posting
            try:
                full_url = (li.find('a', class_='base-card--link') or li.find('a', class_='base-card__full-link'))['href']
                urn = (li.find('a', class_='base-card--link') or li.find('div', class_='base-search-card--link'))['data-entity-urn']
            except Exception:
                print(li)
            job_id = urn.split(':')[3]

            # Get the actual job posting
            posting_response = requests.get(full_url)

            # parse job posting
            test_posting = '<div class="show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden"> <p>We are seeking entry-level software developers 3 yoe interested in joining our team of innovators and working remotely with us to delve into our application architecture. You will construct applications from the foundation up while also improving an established core. You will be afforded the opportunity to collaborate in compact yet comprehensive teams that possess absolute authority over modules and applications.</p><p><br/></p><p>Duties and obligations:</p><p><br/></p><p>   Develops, tests, debugs, and implements custom applications in C# that utilize microservices techniques and Angular 2+ in a.Net environment.</p><p>   Employs SQL to retrieve, query, and join data when required with TSQL.</p><p>   Potentially integrates multiple components across disparate applications</p><p>   Content creator for technical specifications and additional documentation</p><p>   Innovates processes and instruments that facilitate and accelerate the attainment of development objectives.</p><p>   Works in conjunction with various technical teams (DevOps, Database, QA Testers, Analysts) to guarantee the effective execution of projects, encompassing testing, integration, and deployment.</p><p><br/></p><p><br/></p><p><br/></p><p>Essential Qualifications:</p><p><br/></p><p>   Bachelor\'s degree from an accredited institution in the United States in computer science or a related field.</p><p>   Fundamental expertise in object-oriented technology and contemporary user interfaces, including SQL</p><p>       Software development life cycles, coding standards, code reviews, source control administration, and testing; Agile and waterfall</p><p>   Outstanding written and verbal communication abilities.</p><p><br/></p><p><br/></p><p><br/></p><p><br/></p>'
            posting_soup = BeautifulSoup(test_posting, 'html.parser')
            job_description = posting_soup.find('div', class_='show-more-less-html__markup')
            # Get all the <p> tags
            p_tags = job_description.find_all('p')
            # Join all the text from the <p> tags
            posting_text = ' '.join(p_tag.get_text() for p_tag in p_tags)
            print(posting_text)
            # Define a regex pattern to find mentions of greater than 3 years of experience
            pattern = r'(\d{1,2,3}\+?)(\s|-)*(years|yrs|yoe)'

            # Find all matches in the text
            matches = re.findall(pattern, posting_text, re.IGNORECASE)

            if len(matches) < 0:
                # Send a push notification
                job_url = '{base_url}{job_id}'.format(base_url=base_url_job_link, job_id=job_id)
                title = '-title "{}"'.format(job_title)
                subtitle = '-subtitle "{}"'.format(company)
                url = '-open ' + job_url
                command = base_command + ' ' + title + ' ' + subtitle + ' ' + message + ' ' + url + ' ' + app_icon
                os.system(command)
                play_sound = True
    if play_sound:
        # replace this with your sound of choice
        os.system('afplay honk.aiff')

def main():
    filter_jobs(soup)

if __name__ == '__main__':
    main()