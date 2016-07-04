#!/usr/bin/python

"""
create-iam-user - CLI tool to easily create IAM user and format on-boarding email template

Usage:
  create-iam-user -u <username> -a <account>
  create-iam-user [ -h | --help | --version ]

Options:
  --version              Show version.
  -h --help              Show this screen.
  -u --user USER         Specify username to create
  -a --account ACCOUNT   Specifies AWS Account
"""

from boto3 import resource
from docopt import DocoptExit, docopt
from string import ascii_letters, punctuation, digits
from random import randint, choice


def main():
    try:
        docopt_args = docopt(__doc__, version='Create IAM User v1.0')

        create_user(**docopt_args)
        create_access_key_pair(**docopt_args)
        create_login_profile(**docopt_args)

    except DocoptExit as e:
        print e.message


def create_user(args):
    username = args['<username>']
    account = args['<account>']

    iam = resource('iam').User('name')
    response = iam.create(Path='arn:aws:iam::{0}:{1}'.format(username, account))

    return response


def create_access_key_pair(args):
    username = args['<username>']

    iam = resource('iam').User(username)
    response = iam.create_access_key_pair()
    return response


def create_login_profile(args):
    username = args['<username>']
    password = generate_password()

    iam = resource('iam').User(username)
    response = iam.create_login_profile(Password=password, PasswordResetRequired=True)
    return response


def generate_password():
    characters = ascii_letters + punctuation + digits
    password = "".join(choice(characters) for x in range(randint(8, 16)))
    return password


if __name__ == "__main__":
    exit(main())