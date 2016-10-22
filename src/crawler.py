import praw
import re

USER = 'neuralcrawler'
SUBREDDITS = ['bodybuilding']
SINCE = 1420070400
SAVE_PATH = 'data/bodybuilding/'
SAVE_INTERVAL = 100

# Only allow clean text
ALLOWED = re.compile(r'^[a-zA-Z0-9\-\./\'\"\(\)\s\?,]+$')

r = praw.Reddit(user_agent=USER)

submissions = list()

for subreddit in SUBREDDITS:
    print subreddit
    submissions += (list(praw.helpers.submissions_between(r, subreddit,
                                                          lowest_timestamp=SINCE,
                                                          newest_first=True)))

data = ''
version = 0
submission_num = 0

def write_file(version):
    with open(SAVE_PATH + str(version) + '.txt', 'w') as f:
        f.write(data)

for submission in submissions:
    try:
        print 'Processing: ' + submission.title
        submission.replace_more_comments(limit=16, threshold=15)

        if submission_num and submission_num % SAVE_INTERVAL == 0:
            write_file(version)
            version += 1

        comments = praw.helpers.flatten_tree(submission.comments)

        for comment in comments:
            try:
                if ALLOWED.match(comment.body.strip('\n')) is not None:
                    data += comment.body.replace('\n', ' ') + '\n'
            except:
                pass

        submission_num += 1
    except Exception, e:
        print e, submission_num, len(data.split('\n'))
        continue

write_file('final')