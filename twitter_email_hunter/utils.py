import re


def extract_email(text, domain):
    res = re.search(r'([^\s\\]*)@{}'.format(domain), text, re.I)
    if res:
        return res.group()


def get_tweet_url(tweet):
    return "https://twitter.com/{author}/status/{id}".format(
        author=tweet.author.screen_name, id=tweet.id)
