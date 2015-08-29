from .utils import extract_email
from .models import Tweets, Result


def search_emails(api, username, domain=None):
    tweets = Tweets(api, username=username)

    while True:
        tweet = next(tweets)
        email = extract_email(tweet.text, domain)
        if email:
            yield Result(email=email, tweet=tweet)
