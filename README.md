# Twitter email hunter

*Use this at your own risk. Try not to invade people's privacy. They don't like it (I've been told so).*

This is a simple tool that will help you locate someone's email address from his/her twitter timeline. I've just tested it with Python3, although a tox setup PR would be highly appreciated.

*To use it you'll need to create your own Twitter app. Go to https://apps.twitter.com/ or https://dev.twitter.com*

# Usage

(preferable inside a virtualenv)

    $ pip install twitter-email-hunter
    $ twitter-email-hunt  -h rmotr_com -d rmotr.com -k [CONSUMER_KEY] -s [SECRET_KEY]

# Testing

    $ python setup.py test
