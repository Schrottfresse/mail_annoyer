#!/usr/bin/env python3

import sched
import time
import configparser
import logging
from email.mime.text import MIMEText
from random import randint
from smtplib import SMTP


def read_subjects(filename):
    global subjects
    file = open(filename)
    subjects = [line.rstrip() for line in file]
    file.close()


def read_config(filename):
    global config
    config = configparser.ConfigParser()
    config.read(filename)


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
            logging.info("Mail with message '" + msg['Subject'] + "' sent!")
    except Exception as exc:
        logging.error(exc)

    rand_time = 1800 + randint(0, 30) * 60
    logging.info("Next mail in " + str(rand_time) + " seconds.")
    s.enter(rand_time, 0, read_config, ("mail.conf", ))
    s.enter(rand_time, 0, read_subjects, ("sprueche.txt", ))
    s.enter(rand_time, 1, send_mail)


config = None
subjects = list()
read_config("mail.conf")
read_subjects("sprueche.txt")

logging.basicConfig(format='%(levelname)s: %(message)s', level=getattr(logging, config['log']['level'].upper(), None))
logging.debug("Read subjects.")
logging.debug("Read config")

s = sched.scheduler()
s.enter(2, 0, send_mail)
s.run()
logging.debug("Started scheduler.")
