from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

import urllib, json
import unicodedata
import feedparser
from bs4 import BeautifulSoup

__author__ = 'James Purser'

LOGGER = getLogger(__name__)

class AngryBeanieSkill(MycroftSkill):
    def __init__(self):
        super(AngryBeanieSkill, self).__init__(name="AngryBeanieSkill")

    def initialize(self):
        get_podcasts_intent = IntentBuilder("GetPodcastsIntent").require("GetPodcastsKeyword").build()
        self.register_intent(get_podcasts_intent, self.handle_get_podcasts_intent)

        get_episodes_intent = IntentBuilder("GetEpisodesIntent").require("GetEpisodesKeyword").require("ShowName").build()
        self.register_intent(get_episodes_intent, self.handle_get_episodes_intent)

    def handle_get_podcasts_intent(self, message):
        self.speak_dialog("podcasts")

    def handle_get_episodes_intent(self, message):
        show = message.data.get("ShowName")
        #episodes = "Hello world"
        episodes = getEpisodes(show.encode('utf-8'))
        self.speak(show.encode('utf-8'))
        self.speak_dialog("episodes", {'show': show.encode('utf-8'), 'episodes': episodes.encode('utf-8')})

def getEpisodes(show):
    feeds = {'for science': 'http://feeds.feedburner.com/angrybeanie/ForScienceMP3?format=xml', 'women in stemm': 'http://feeds.feedburner.com/WomenInStemm?format=xml'}

    feed = feedparser.parse(feeds[show])
    titles = ""
    for entry in feed.entries:
        titles += entry.title+", "

    return titles

def create_skill():
    return AngryBeanieSkill()
