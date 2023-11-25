import sys

timing = sys.argv[0]
#region *** site config definitions ***
supported_sites = ['linkedin', 'indeed']

class SiteConfig:
    def __init__(self, site):
        self.site = site
        self._base_url = self.get_base_url()

    def get_base_url(self):
        # TODO: figure out system for sorting sites
        return 'http://www.linkedin.com' if self.site == 'linkedin' else 'http://www.indeed.com'

    @property
    def base_url(self):
        return self._base_url

#endregion *** ****

#region *** function definitions ***
def search_site(config) -> preview_cards:
    # queries site(s) for jobs
    # returns a bunch of preview cards

def create_notification() -> notification_obj:
def filter_title():

# initial title filter from preview cards

# if it passes title filter, get posting
def get_posting(url):

# get full description for jobs that pass the initial filters
# returns descriptions

def filter_description():


def push_notification():


def play_alert():
    # HONK

def save_notifications:


def get_notifications:
    all_notifications = []
    for site in supported_sites:
        config = SiteConfig(site)

        search_response = search_site(config)

        site_notifications = filter_response(config, search_response)
        all_notifications = all_notifications + site_notifications
    return all_notifications


def filter_response(config, preview_cards) -> notifications:
    notifications = []
    for card in preview_cards:
        filter_title(card)

        # if it passes title filter, get posting
        posting = get_posting(url)

        filter_description(posting)

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
