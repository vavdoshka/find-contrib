from itertools import chain
import json
import datetime
import time
from github import Github
try:
    import telepot
except ImportError:
    pass

CONFIG = json.load(open("./config.json"))
LABELS = CONFIG["search"]["labels"]
LANGUAGE = CONFIG["search"]["language"]

ISSUE_CREATED_AT = datetime.datetime.now() -\
                   datetime.timedelta(days=int(CONFIG["search"]['DaysDelta']))
SEARCH_QUERY = "type:issue language:{language} " \
               "state:open no:assignee label:{label} created:>={date}"

class TelegramPublisher(object):


    def __init__(self):
        self.bot = telepot.Bot(CONFIG["publishers"][0]["token"])

    def send_message(self, msg):
        self.bot.sendMessage(CONFIG["publishers"][0]["chat_id"], msg)

class IssueProxy(object):

    def __init__(self, issue):
        self._issue = issue

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
        {0._issue.html_url}
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
    tb = TelegramPublisher()
    for issue in issues:
        tb.send_message(str(issue))

main()
# TODO: prettify output
# TODO: cron this.