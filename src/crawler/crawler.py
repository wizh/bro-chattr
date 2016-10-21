import praw
import re

USER = 'neuralcrawler'
SUBREDDIT = 'bodybuilding'
SAVE_INTERVAL = 100

# Only allow clean text
ALLOWED = re.compile(r'^[a-zA-Z0-9\-\./\'\"\(\)\s\?,]+$')

r = praw.Reddit(user_agent=USER)

submissions = praw.helpers.submissions_between(r, SUBREDDIT, newest_first=True)

data = ''
version = 0
submission_num = 0

def write_file(version):
    with open('data/' + str(version) + '.txt', 'w') as f:
        f.write(data)

for submission in submissions:
    if submission_num and submission_num % SAVE_INTERVAL == 0:
        write_file(version)
        version += 1

    comments = praw.helpers.flatten_tree(submission.comments)
    for comment in comments:
        try:
            if ALLOWED.match(comment.body.strip('\n')) is not None:
                data += comment.body + '\n\n'
        except:
            pass

    submission_num += 1

write_file('final')