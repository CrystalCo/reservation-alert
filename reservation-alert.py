#!/usr/bin/env python3

import os
import json
import time
import requests
import smtplib, ssl
import argparse
import logging
from lxml import html
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(url, email_info):
    PORT = 465
    PW = input('Type your password and press enter: ')
    FROM_EMAIL = email_info['from']
    TO_EMAIL = email_info['to']

    message = MIMEMultipart("alternative")
    message["Subject"] = "Noma Reservation available"
    message["From"] = FROM_EMAIL
    message["To"] = TO_EMAIL
    text = 'Noma has bookings available !! URL to book reservations: %s' % url

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    try:
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
            server.login(email_info['to'], PW)
            logger.info('Logged in! Composing message..')
            server.sendmail(FROM_EMAIL, TO_EMAIL, message.as_string())
            logger.info('Message has been sent.')

    except Exception as e:
        logger.info('Failed to login')
        logger.info(e)


def detect_booking(url):
    r = requests.Session().get(url, headers={
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    })
    r.raise_for_status()
    tree = html.document_fromstring(r.text)
    book_now = 'book now'

    try:
        button_strings = tree.find_class('MuiButton-label')
        button_strings = [s.text.lower() for s in button_strings]
        logger.info(button_strings)

        book_now_strings = [s for s in button_strings if book_now in s]
        # extract the status from the string
        status = len(book_now_strings) > 0
        return status
    except (IndexError, TypeError) as e:
        logger.debug(e)
        logger.info('Didn\'t find the \'book now\' element, trying again later')


def get_config(config):
    with open(config, 'r') as f:
        return json.loads(f.read())


def config_logger(debug):
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    handler = logging.StreamHandler()
    logger.addHandler(handler)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        default='%s/config.json' % os.path.dirname(
                            os.path.realpath(__file__)),
                        help='Configuration file path')
    parser.add_argument('-t', '--poll-interval', type=int, default=30,
                        help='Time in seconds between checks')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debug level logging')
    return parser.parse_args()


def main():
    args = parse_args()
    config_logger(args.debug)
    config = get_config(args.config)
    sold_out = True

    while sold_out:
        logger.info('Checking if booking button enable for %s' % config['base_url'])
        status = detect_booking(config['base_url'])
        if not status:
            logger.info('Booking status is %s. Ignoring...' % status)
            logger.info('Sleeping for %d seconds' % args.poll_interval)
            time.sleep(args.poll_interval)
            continue
        else:
            logger.info('Booking is available!! Trying to send email...')
            send_email(config['base_url'], config['email'])
            sold_out = False

    logger.info('Noma status alert triggered, exiting.')


if __name__ == '__main__':
    main()
