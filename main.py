#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import string
import time
import tweepy
from tweepy.error import TweepError
import unicodedata

# constants
twitter = {
    "self_id": "<your id>",
    "self_url": "https://twitter.com/<username>/status/",
    "consumer_key": "<consumer key>",
    "consumer_secret": "<consumer secret>",
    "access_token": "<access token>",
    "access_token_secret": "<access token secret>",
    "maxlen": 140
}

FILTER_PATH = "filter.txt"
ANS_PATH = "answers.txt"
LOG_PATH = "log.txt"
REPLACEMENTS = {
    "@": '',
    "&euro;": '',
    "&amp;": '',
    "&lt;": '',
    "&gt;": '',
    "&micro;": '',
    "trump": 'drumpf'
}
# necessary functions
def load_answers():

    global ANS_PATH
    try:
        with open(ANS_PATH, 'r') as f:
            answerv = f.read().split('\n')
        # the length management is optional
        return answerv if len(answerv) <= 100 else answerv[-300:]
    except Exception:
        return []


def login():

    global twitter

    auth = tweepy.OAuthHandler(twitter["consumer_key"], twitter["consumer_secret"])
    auth.set_access_token(twitter["access_token"], twitter["access_token_secret"])
    return tweepy.API(auth)


def update_log(msg):

    global LOG_PATH

    with open(LOG_PATH, 'a') as log:
        log.write(
        str(msg.sender.id) + " | " + str(msg.sender.screen_name) + " ; \"" + str(msg.text) + "\"\n"
        )


def is_connected():
    property
    REMOTE_SERVER = "www.twitter.com"
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        return True
    except Exception:
        return False


def update_answers(answer, answers):

    global ANS_PATH

    answer = str(answer)
    with open(ANS_PATH, 'a') as ansf:
        ansf.write(answer + '\n')
        return answers + [answer]


def load_filter():

    global FILTER_PATH

    try:
        with open(FILTER_PATH, 'r') as filter:
            return [w.strip() if w.strip() else "voldemort" for w in filter.read().split('\n')]
    except Exception:
        return []

# I don't even remember why I did this
def read_tweet(msg):
    msglist = []
    if msg.count("\"") == 0 or msg.count("\"") == 1:
        return [""]
    newmsg = ""
    including  = False
    for char in msg:
        if char == "\"" and including:
            including = False
            msglist.append(newmsg)
            newmsg = ""
        elif char == "\"" and  not including:
            including = True
        elif including:
            newmsg += char
    return msglist


def has_phone_numbers(tweet):  # possibly
    # this was a personal request
    tweet = tweet.replace(' ', '')
    for i in range(len(tweet)-4):
        if tweet[i:i+3].isdigit():
            return True
    return False


# vars
try:
    last_tweet = []
    with open(ANS_PATH, 'r') as f:
        l = f.readline().strip()
        if l:
            last_tweet.append(l)
        last_tweet = last_tweet[-1]
except Exception:
    last_tweet = ''
answers = load_answers()


def twitter_loop():

    global REPLACEMENTS, answers, last_tweet, witter

    while 1:  # loop for logging
        try:
            api = login()
            break
        except Exception:
            time.sleep(5)

    try:
        msg = api.direct_messages(since_id=last_tweet, full_text=True)[-1]
    except IndexError:
        time.sleep(20)
    except Exception as ex:
        raise ex
    last_tweet = msg.id
    answers = update_answers(msg.id, answers)

    # what is this?
    msg.text = read_tweet(msg.text.strip().lower())[0]

    # fix html escapes, remove mentions and replace drumpf with trump
    for key in REPLACEMENTS:
        msg.text = msg.text.replace(key, REPLACEMENTS[key])

    # tweet length
    if len(msg.text.strip()) == 0 or len(msg.text.strip()) >= twitter["maxlen"]:
        return

    if has_phone_numbers(msg.text):
        return

    # is already answered
    if msg.id in answers:
        return

    # remove spaces for filter check
    for word in filter_words:
        if word.replace(' ', '') in msg.text.replace(' ', ''):
            return

    # sorcery
    if word.replace(' ', '') in "".join(
        x for x in unicodedata.normalize(
        'NFKD', msg.text) if x in string.ascii_letters
        ).lower().replace(' ', ''):
        return

    # check connection
    while not is_connected():
        time.sleep(5)
    try:
        api.update_status(msg.text)
        update_log(msg)
        api.send_direct_message(user_id=msg.sender.id,
        text=twitter["self_url"] + str(
        api.user_timeline(id=twitter["self_id"], count=1)[0].id)
        )
        time.sleep(60)
    except TweepError:
        pass



# Main function
if __name__ == "__main__":

    filter_words = load_filter()

    while 1:
        try:
            twitter_loop()
        except Exception:
            time.sleep(5 * 60) # wait for API rate cooldown
