#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import string
import time
import tweepy
import unicodedata


# constants
twitter = {
    "self_id": "724654853436350464",
    "self_url": "https://twitter.com/EPT_bot/status/",
    "consumer_key": "dfm56mbMwj84ZBkiSniEi11dj",
    "consumer_secret": "aOYSyONsbyG4kfJ1VOYVs0Y3KJblfyCsLevAILGbvRKsrMFpCv",
    "access_token": "724654853436350464-gztpaaWM9cOAGWTAb7KiTwtezKhjQx6",
    "access_token_secret": "XIuF6CDDmA1Mnpiq5sLac2CmsZYpdCtGBfAA0xCIVtp6p",
    "maxlen": 140
}

LMID_PATH = "/path/to/last/message"
FILTER_PATH = "/path/to/filter"
ANS_PATH = "/path/to/answer"
LOG_PATH = "/path/to/log"
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
    with open(ANS_PATH, 'r') as f:
        answerv = f.read().split('\n')
    # the length management is optional
    return answerv if len(answerv) <= 100 else answerv[-300:]

def login():

    global twitter

    auth = tweepy.OAuthHandler(twitter["consumer_key"], twitter["consumer_secret"])
    auth.set_access_token(twitter["access_token"], twitter["access_token_secret"])
    return tweepy.API(auth)


def update_log(msg, tweet):

    global LOG_PATH

    with open(LOG_PATH, 'a') as log:
        log.write(
        str(msg.sender.id) + " | " + str(msg.sender.screen_name) + " ; \"" + str(tweet) + "\"\n"
        )


def is_connected():
    REMOTE_SERVER = "www.twitter.com"
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        return True
    except Exception:
        return False


def update_answers(answer, answers):

    global ANS_PATH

    with open(ANS_PATH, 'a') as ansf:
        ansf.write(answer)
        return answers + [answer]


def load_filter():

    global FILTER_PATH

    with open(FILTER_PATH, 'r') as filter:
        return filter.read().split('\n')


# I don't even remember why I did this
def read_tweet(msg):
    msglist = []
    if msg.count("\"") == 0 or msg.count("\"") == 1:
        return [""]
    newmsg = ""
    including  = False
    for char in msg:
        if char == "\"" and includig:
            includig = False
            msglist.append(newmsg)
            newmsg = ""
        elif char == "\"" and  not including:
            includig = True
        elif includig:
            newmsg += char
    return msglist


def has_phone_numbers(tweet):  # possibly
    # this was a personal request
    tweet = tweet.replace(' ', '')
    for i in range(len(tweet)-3):
        if tweet[i:i+3].isdigit():
            return True
    return False


# vars
last_tweet = ''
answers = load_answers()


def twitter_loop():

    global REPLACEMENTS, answers, twitter

    while 1:  # loop for logging
        try:
            api = login()
            break
        except Exception:
            time.sleep(5)

    msg = api.direct_messages(since_id=last_tweet, full_text=True)[-1]
    last_tweet = msg.id
    answers = update_answers(msg.id, answers)

    # what is this?
    msg.text = read_tweet(msg.text.strip().lower())[0]

    # fix html escapes, remove mentions and replace drumpf with trump
    for key in REPLACEMENTS:
        msg.text = msg.text.replace(key, REPLACEMENTS[key])

    # tweet length
    if len(msg.text.strip()) == 0 or len(msg.text.strip()) >= twitter[maxlen]:
        return


    if has_phone_numbers(message.text):
        return

    # is already answered
    if msg.id in answers:
        return

    # remove spaces for filter check
    for word in filter_words:
        if word.replace(' ', '') in msg.text.replace(' ', ''):
            return

    # sorcery
    if word.repalce(' ', '') in "".join(
        x for x in unicodedata.normalize(
        'NFKD', tweet) if x in string.ascii_letters
        ).lower().replace(' ', ''):
        return

    # check connection
    while not is_connected():
        time.sleep(5)
    api.update_status(msg.text)
    update_log(msg)
    api.send_direct_message(user_id=sender_id,
    text=twitter["self_url"] + str(
    api.user_timeline(id=twitter["own_id"], count=1)[0].id)
    )
    time.sleep(60)



# Main function
if __name__ == "__main__":

    filter_words = load_filter()

    while 1:
        try:
            twitter_loop()
        except Exception:
            time.sleep(5 * 60) # wait for API rate cooldown
