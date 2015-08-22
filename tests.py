import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from tweepy import API
from tweepy.models import Status, User

from twitter_email_hunter import search_emails
from twitter_email_hunter.utils import extract_email
from twitter_email_hunter.models import Tweets, Result


def test_matcher():
    text = 'Some text test-1@example.com'
    assert 'test-1@example.com' == extract_email(text, 'example.com')

    text = 'Some text test-1@example.com with something at the end'
    assert 'test-1@example.com' == extract_email(text, 'example.com')

    text = ('Some text test-1@example.com with something at the'
            'end and other email like john@example.com')
    assert 'test-1@example.com' == extract_email(text, 'example.com')

    text = ('Some text test-1@example1.com with something at the'
            'end and other email like john@example.com')
    assert 'john@example.com' == extract_email(text, 'example.com')

    text = 'test-1@example.com at the begginning'
    assert 'test-1@example.com' == extract_email(text, 'example.com')


class TweetsIteratorTestCase(unittest.TestCase):
    def test_iterator_requests_tweets_for_the_first_time(self):
        with mock.patch.object(API, 'user_timeline') as m:
            api = API()
            mocked_tweets = [
                mock.MagicMock(spec=Status, id=1),
                mock.MagicMock(spec=Status, id=2),
                mock.MagicMock(spec=Status, id=3),
            ]
            m.return_value = mocked_tweets
            tweets = Tweets(api=api, username="rmotr_com")
            self.assertEqual(next(tweets), mocked_tweets[0])
            self.assertEqual(next(tweets), mocked_tweets[1])
            self.assertEqual(next(tweets), mocked_tweets[2])

        m.assert_called_once_with('rmotr_com', count=200)

    def test_iterator_paginates_time(self):
        with mock.patch.object(API, 'user_timeline') as m:
            api = API()
            mocked_tweets_page_1 = [
                mock.MagicMock(spec=Status, id=1),
                mock.MagicMock(spec=Status, id=2),
                mock.MagicMock(spec=Status, id=3),
            ]
            m.return_value = mocked_tweets_page_1
            tweets = Tweets(api=api, username="rmotr_com", count=3)
            self.assertEqual(next(tweets).id, 1)
            self.assertEqual(next(tweets).id, 2)
            self.assertEqual(next(tweets).id, 3)

            m.assert_called_once_with('rmotr_com', count=3)
            m.reset_mock()
            mocked_tweets_page_2 = [
                mock.MagicMock(spec=Status, id=3),  # API repeats lasts tweet
                mock.MagicMock(spec=Status, id=4),
                mock.MagicMock(spec=Status, id=5),
            ]
            m.return_value = mocked_tweets_page_2

            self.assertEqual(next(tweets).id, 4)
            self.assertEqual(next(tweets).id, 5)
            m.assert_called_once_with('rmotr_com', max_id=3, count=3)


class SearchEmailTestCase(unittest.TestCase):
    def test_search_email_finds_email(self):
        api = mock.MagicMock(spec=API)

        iteration = {'counter': -1}
        mocked_tweets = [
            mock.MagicMock(spec=Status, id=1, text="???"),
            mock.MagicMock(
                spec=Status, id=2,
                text="Tweet text santiago@rmotr.com.",
                author=mock.MagicMock(spec=User, screen_name='rmotr_com')),
            mock.MagicMock(spec=Status, id=3, text="???")
        ]

        def _next(_self):
            iteration['counter'] += 1
            return mocked_tweets[iteration['counter']]

        with mock.patch.object(Tweets, '__next__', new=_next):

            results = search_emails(api, 'rmotr_com', 'rmotr.com')
            result = next(results)
            self.assertIsNotNone(result)
            self.assertEqual(result.tweet, mocked_tweets[1])
            self.assertEqual(result.email, 'santiago@rmotr.com')


class ResultTestCase(unittest.TestCase):
    def test_result_equality(self):
        "A result should be equal if contains the same email"
        author1 = mock.MagicMock(spec=User, screen_name='rmotr_com')
        author2 = mock.MagicMock(spec=User, screen_name='santiagobasulto')
        self.assertEqual(
            Result(email='questions@rmotr.com',
                   tweet=mock.MagicMock(spec=Status, id=1,
                                        text="???", author=author1)),
            Result(email='questions@rmotr.com',
                   tweet=mock.MagicMock(spec=Status, id=2,
                                        text="xxx", author=author2)),
        )

        tweet = mock.MagicMock(spec=Status, id=1, text="???", author=author2)
        self.assertEqual(
            Result(email='questions@rmotr.com', tweet=tweet),
            Result(email='questions@rmotr.com', tweet=tweet),
        )

        self.assertNotEqual(
            Result(email='questions@rmotr.com', tweet=tweet),
            Result(email='santiago@rmotr.com', tweet=tweet),
        )

        result_list = [
            Result(email='questions@rmotr.com', tweet=tweet),
            Result(email='santiago@rmotr.com', tweet=tweet),
            Result(email='martin@rmotr.com', tweet=tweet)
        ]
        self.assertTrue('questions@rmotr.com' in result_list)
