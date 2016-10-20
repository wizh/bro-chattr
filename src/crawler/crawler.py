import praw
import re

USER = 'neuralcrawler'
SUBREDDIT = 'bodybuilding'

# Only allow clean text
ALLOWED = re.compile(r'^[a-zA-Z0-9\-\./\'\"\(\)\s\?,]+$')

r = praw.Reddit(user_agent=USER)

submissions = praw.helpers.submissions_between(r, SUBREDDIT, newest_first=True)

data = ''

for submission in submissions:
    comments = praw.helpers.flatten_tree(submission.comments)
    for comment in comments:
        try:
            if ALLOWED.match(comment.body.strip('\n')) is not None:
                data += comment.body + '\n\n'
        except:
            pass

with open('data.txt', 'w') as f:
    f.write(data)