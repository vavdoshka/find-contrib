from itertools import chain
import json
import datetime
import time
from github import Github

CONFIG = json.load(open("./config.json"))
LABELS = CONFIG["search"]["labels"]
LANGUAGE = CONFIG["search"]["language"]

ISSUE_CREATED_AT = datetime.datetime.now() -\
                   datetime.timedelta(days=int(CONFIG["search"]['DaysDelta']))
SEARCH_QUERY = "type:issue language:{language} " \
               "state:open no:assignee label:{label} created:>={date}"


class IssueProxy(object):

    def __init__(self, issue):
        self._issue = issue

    @property
    def issue_url(self):
        return self._issue.url

    @property
    def issue_title(self):
        return self._issue.title

    @property
    def comments_count(self):
        return self._issue.comments

    @property
    def labels(self):
        return [label.name for label in self._issue.labels]

    @property
    def repository_identity(self):
        return self._issue.repository.name


    @property
    def repository_stars_count(self):
        return self._issue.repository.stargazers_count

    @property
    def repository_forks_count(self):
        return self._issue.repository.forks_count

    def __str__(self):
        return """
        Title: {0.issue_title}
        Url: {0.issue_url}
        Labels: {0.labels}
        Comments Count: {0.comments_count}

        Repository Name: {0.repository_identity}
        Repository Stars Count: {0.repository_stars_count}
        Repository Forks Count: {0.repository_forks_count}
        """.format(self)


def main():
    g_session = Github(CONFIG["auth"]['user'], CONFIG["auth"]['password'])
    results = []
    for label in LABELS:
        results.append(g_session.search_issues(
            SEARCH_QUERY.format(label=label,
                                date=time.strftime("%Y-%m-%d",
                                                   ISSUE_CREATED_AT.timetuple()),
                                language=LANGUAGE)))

    issues = [IssueProxy(issue) for issue in (chain(*results))]

# TODO: throw a message to telgramm + email?
# TODO: cron this.