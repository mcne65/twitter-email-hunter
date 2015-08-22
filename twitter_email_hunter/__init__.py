__title__ = 'twitter_email_hunter'
__version__ = '1.0'
__author__ = 'Santiago Basulto'
__email__ = 'santiago@rmotr.com'
__license__ = 'MIT'
__description__ = "Search for email addresses in a twitter timeline"

try:
    input = raw_input
except NameError:
    pass

__all__ = ['search_emails']


from .utils import extract_email
from .models import Tweets, Result


def search_emails(api, username, domain):
    tweets = Tweets(api, username=username)

    while True:
        tweet = next(tweets)
        if '@' + domain in tweet.text:
            email = extract_email(tweet.text, domain)
            yield Result(email=email, tweet=tweet)
