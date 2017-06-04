import time
from github import Github

g_session = Github("", "")
current_date = time.strftime("%Y-%m-%d")
labels = ["easy", "beginner"]
search_query = "type:issue language:JavaScript state:open no:assignee label:{label} created:>={date}"

results = []
for label in labels:
    results.append(g_session.search_issues(search_query.format(label=label, date=current_date)))

# TODO: enhance list of labels merge the results, throw a message to telgramm + email?
# TODO: cron this.