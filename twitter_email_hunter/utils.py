import re


def extract_email(text, domain=None):
    pattern = r'([^\s\\(\{\[]*)'
    domain_pattern = r'(\w+\.)*(\w+)\.(\w+)(\/.*)?'
    if domain:
        regexp = pattern + r'@{}'.format(domain)
    else:
        regexp = pattern + r'@' + domain_pattern

    res = re.search(regexp, text, re.I)
    if res:
        return res.group()


def get_tweet_url(tweet):
    return "https://twitter.com/{author}/status/{id}".format(
        author=tweet.author.screen_name, id=tweet.id)
