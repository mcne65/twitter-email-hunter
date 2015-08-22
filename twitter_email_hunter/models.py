from .utils import get_tweet_url


class Tweets(object):
    def __init__(self, api, username=None, user_id=None, user=None, count=200):
        if not any([username, user_id, user]):
            raise AttributeError("You must specify a user")

        self.api = api
        self.username = username
        self.last_max_id = None
        self.count = count
        self.tweets = None

        self.pointer = None
        self.limit = None

    def _consume_tweets(self):
        if self.last_max_id:
            self.tweets = self.api.user_timeline(
                self.username, max_id=self.last_max_id, count=self.count)
            self.tweets = self.tweets[1:]
        else:
            self.tweets = self.api.user_timeline(
                self.username, count=self.count)

        if not self.tweets:
            raise StopIteration()

        self.last_max_id = self.tweets[-1].id
        self.pointer = 0
        self.limit = len(self.tweets)

    def are_tweets_available(self):
        return self.tweets and self.pointer < self.limit

    def __next__(self):
        if not self.are_tweets_available():
            self._consume_tweets()

        tweet = self.tweets[self.pointer]
        self.pointer += 1
        return tweet

    def __iter__(self):
        return self

    next = __next__


class Result(object):
    def __init__(self, email, tweet):
        self.email = email
        self.tweet = tweet
        self.tweet.full_url = get_tweet_url(tweet)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.email == other.email
        elif isinstance(other, str):
            return self.email == other
