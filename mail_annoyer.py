#!/usr/bin/env python3

import sched
import time
import configparser
import logging
from email.mime.text import MIMEText
from random import randint
from smtplib import SMTP


def read_subjects(filename):
    file = open(filename)
    result = [line.rstrip() for line in file]
    file.close()
    return result


def random_subject(subjects):
    return subjects[randint(0, len(subjects) - 1)]


def send_mail():
    msg = MIMEText("-kT-", 'plain')
    msg['Subject'] = random_subject(subjects)
    msg['From'] = config['mail']['user']
    msg['To'] = config['mail']['to']

    try:
        conn = SMTP(config['mail']['addr'] + ':' + config['mail']['port'])
        conn.starttls()
        conn.login(config['mail']['user'], config['mail']['pass'])
        try:
            conn.send_message(msg)
        finally:
            conn.quit()
    except Exception as exc:
        logging.error(exc)

    rand_minute = randint(0,30)*60
    s.enter(1800+rand_minute)


subjects = read_subjects('sprueche.txt')
config = configparser.ConfigParser()
config.read("mail.conf")
logging.basicConfig(format='%(levelname)s: %(message)s', level=getattr(logging, config['log']['level'].upper(), None))

send_mail()

s = sched.scheduler()
s.enter(2, 0, send_mail)
s.run()
