import sys
import tweepy
import click
from twitter_email_hunter import search_emails


def show_results(results):
    if not results:
        click.echo("\n:'( No results")
        return

    click.echo("\n##### Successful Hunt! Here are your emails #####")
    click.echo("------------------------------------\n")
    for result in results:
        click.echo("Email: '{}'".format(result.email))
        click.echo("Tweet id: {}".format(result.tweet.id))
        click.echo("Tweet URL: {}".format(result.tweet.full_url))
        click.echo("------------------------------------")


@click.command(help="Search for emails from a twitter profile")
@click.option('--handle', '-h', required=True,
              help="Twitter handle (eg: @rmotr_com).")
@click.option('--domain', '-d', required=False,
              help="Will look for emails just with that domain")
@click.option('--consumer-key', '-k',
              envvar='TWITTER_CONSUMER_KEY', required=True,
              help="Create an app and get your keys from dev.twitter.com")
@click.option('--secret-key', '-s',
              envvar='TWITTER_SECRET_KEY', required=True,
              help="Create an app and get your keys from dev.twitter.com")
@click.option('--interactive/--no-interactive', default=False,
              help="The script will print everytime it "
              "finds an email address and will ask if you want to stop it.")
def interactive_search_emails(handle, domain, consumer_key,
                              secret_key, interactive):
    auth = tweepy.AppAuthHandler(consumer_key, secret_key)
    api = tweepy.API(auth)
    results = []
    msg = "I've just found '{}'. Should I stop now?"

    try:
        for result in search_emails(api, handle, domain):
            if result not in results:
                results.append(result)
                if not interactive:
                    click.echo("Found {}".format(result.email))
                    continue
                if click.confirm(msg.format(result.email)):
                    raise KeyboardInterrupt()
    except KeyboardInterrupt:
        show_results(results)
        sys.exit(0)
    else:
        show_results(results)


if __name__ == '__main__':
    interactive_search_emails()
