# Twitter email hunter

**Use this at your own risk. Try not to invade people's privacy. They don't like it (I've been told so).**

This is a simple tool that will help you locate email addresses from a twitter timeline. I've just tested it with Python3, although a tox setup PR would be highly appreciated.

*To use it you'll need to create your own Twitter app. Go to https://apps.twitter.com/ or https://dev.twitter.com*


# Installation

(preferable inside a virtualenv)

    $ pip install twitter-email-hunter

You can set your twitter keys as environment variables to ease usage. See section below.

# Usages and examples

There are two main modes you can choose *interactive* (default) and *non-interactive*. **Interactive** mode will stop every time it finds an email and will ask you if you want to keep looking, and it'll report after it's done.
**Non interactive** will just process until you stop the script with Ctrl-C. It'll show a report after you kill it.

Look for any emails on our timeline (interactive):

    $ twitter-email-hunt -h rmotr_com -k [CONSUMER_KEY] -s [SECRET_KEY] --interactive

![http://i.imgur.com/2bTIEnr.png](http://i.imgur.com/2bTIEnr.png)

Look for any emails on our timeline that are just from our domain (interactive):

    $ twitter-email-hunt -h rmotr_com -d rmotr.com -k [CONSUMER_KEY] -s [SECRET_KEY] --interactive

Non interactive example:

    $ twitter-email-hunt -h rmotr_com -d rmotr.com -k [CONSUMER_KEY] -s [SECRET_KEY]

![http://i.imgur.com/4PHdv2z.png](http://i.imgur.com/4PHdv2z.png)

# Twitter keys

You'll need an app created on twitter to use this tool. You can create it on https://apps.twitter.com/. After you have your keys you can always set them as environment variables to ease usage:

    export TWITTER_CONSUMER_KEY=[CONSUMER_KEY]
    export TWITTER_SECRET_KEY=[SECRET_KEY]

# Testing

    $ python setup.py test
