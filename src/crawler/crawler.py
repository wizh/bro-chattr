import praw
import re

USER = 'neuralcrawler'
SUBREDDIT = 'bodybuilding'

# Only allow clean text
ALLOWED = re.compile(r'^[a-zA-Z0-9\-\./\'\"\(\)\s\?,]+$')

r = praw.Reddit(user_agent=USER)

submissions = praw.helpers.submissions_between(r, SUBREDDIT, newest_first=True)

for submission in submissions:
    comments = praw.helpers.flatten_tree(submission.comments)
    print 'Post:' + submission.title + ':'

    for comment in comments:
        try:
            if ALLOWED.match(comment.body.strip('\n')) is not None:
                print "Comment: " + comment.body + '\n'
        except:
            pass