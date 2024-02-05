class MissingValueError(Exception):
    def __init__(self, message="Could not find value"):
        self.message = message


class JobObject:
    def __init__(self, data={}):
        self.company = data['company'] or ''
        self.description = data['description'] or ''
        self.location = data['location'] or ''
        self.salary = data['salary'] or ''
        self.site = data['site'] or ''
        self.title = data['title'] or ''
        self.url = data['url'] or ''
