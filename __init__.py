from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

import urllib, json
import unicodedata
from bs4 import BeautifulSoup

__author__ = 'James Purser'

LOGGER = getLogger(__name__)

class AngryBeanieSkill(MycroftSkill):
    def __init__(self):
        super(AngryBeanieSkill, self).__init__(name="AngryBeanieSkill")

    def initialize(self):
        get_podcasts_intent = IntentBuilder("GetPodcastsIntent").require("GetPodcastsKeyword").build()
        self.register_intent(get_podcasts_intent, self.handle_get_podcasts_intent)

    def handle_get_podcasts_intent(self, message):
        self.speak_dialog("podcasts")

def create_skill():
    return AngryBeanieSkill()
