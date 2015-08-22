import os
from setuptools import setup
from setuptools.command.test import test as TestCommand

import twitter_email_hunter

version = twitter_email_hunter.__version__
project_name = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
project_url = 'http://github.com/rmotr_com/{project_name}'.format(
    project_name=project_name)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ["--cov", "twitter_email_hunter", "tests.py"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import sys, pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name=twitter_email_hunter.__title__,
    version=version,
    description=twitter_email_hunter.__description__,
    url=project_url,
    download_url="{url}/tarball/{version}".format(
        url=project_url, version=version),
    author=twitter_email_hunter.__author__,
    maintainer=twitter_email_hunter.__author__,
    author_email=twitter_email_hunter.__email__,
    license=twitter_email_hunter.__license__,
    py_modules=['main'],
    packages=['twitter_email_hunter'],
    install_requires=[
        'click==5.1',
        'tweepy==3.4.0',
    ],
    entry_points='''
        [console_scripts]
        twitter-email-hunt=main:interactive_search_emails
    ''',
    tests_require=[
        'cov-core==1.15.0',
        'coverage==3.7.1',
        'py==1.4.30',
        'pytest==2.7.2',
        'pytest-cov==2.0.0',
        'six==1.9.0',
        'mock==1.0.1'
    ],
    zip_safe=True,
    cmdclass={'test': PyTest},
)
