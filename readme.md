Python script to aid in job search.
Supported sites: LinkedIn and Indeed to start with
Filters: titles for keywords + locations, job description for years of experience, clearance requirements
Desktop notifications with custom alert sound
Use crontab to schedule the script to run periodically
Archive list of jobs for recordkeeping

Future features:
Cost analysis: add chatgpt integration to replace manual filters?
Industry filters: avoid marketing, ad solutions, defense etc.
UI + web hosting + email alerts so non-techies can use it as a service
filter out duplicates + multipostings for same job

TODO:
Login to LI / add db to handle duplicate postings
token estimations per day?
Indeed support + refactor
testing

Setup instructions:
1. Copy this repo to your computer
2. Cd into your local copy of the repo and initialize a python environment 
3. Run setup table script in migrations folder to setup database
4. [path to python] [path to job_alert.py] [time in seconds age limit for postings]  

Setup Cronjob (Mac):
1. crontab -e
2. i (insert/type in vi)
3. Example: To run every 15 min between 9am and 5pm
```
*/15 9-17 * * * [path to python] [path to job_alert.py] [time in seconds age limit for postings]
```
4. esc then :wq to save and exit vi