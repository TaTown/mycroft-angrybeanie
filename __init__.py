from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

import urllib, json
import unicodedata
import feedparser
from bs4 import BeautifulSoup

try:
    from mycroft.skills.audioservice import AudioService
except:
    from mycroft.util import play_mp3
    AudioService = None

__author__ = 'James Purser'

LOGGER = getLogger(__name__)

class AngryBeanieSkill(MycroftSkill):
    def __init__(self):
        super(AngryBeanieSkill, self).__init__(name="AngryBeanieSkill")
        self.audioservice = None

    def initialize(self):
        get_podcasts_intent = IntentBuilder("GetPodcastsIntent").require("GetPodcastsKeyword").build()
        self.register_intent(get_podcasts_intent, self.handle_get_podcasts_intent)

        get_episodes_intent = IntentBuilder("GetEpisodesIntent").require("GetEpisodesKeyword").require("ShowName").build()
        self.register_intent(get_episodes_intent, self.handle_get_episodes_intent)
        
        get_latest_episode_intent = IntentBuilder("GetLatestEpisodeIntent").require("GetLatestEpisodeKeyword").require("ShowName").build()
        self.register_intent(get_latest_episode_intent, self.handle_get_latest_episode_intent)
        
        stop_latest_episode_intent = IntentBuilder("StopAngryBeanieIntent").require("AngryBeanieStopVerb").build()
        self.register_intent(stop_latest_episode_intent, self.handle_stop)
        
        if AudioService:
            self.audioservice = AudioService(self.emitter)

    def handle_get_podcasts_intent(self, message):
        self.speak_dialog("podcasts")

    def handle_get_episodes_intent(self, message):
        show = message.data.get("ShowName")
        episodes = getEpisodes(show.encode('utf-8'))
        self.speak_dialog("episodes", {'show': show.encode('utf-8'), 'episodes': episodes.encode('utf-8')})
        
    def handle_get_latest_episode_intent(self, message):
        show = message.data.get("ShowName")
        episode = getLatestEpisode(show)
        self.speak("Playing episode")
        if self.audioservice:
            self.audioservice.play(episode, message.data['utterance'])
        else: # othervice use normal mp3 playback
            self.process = play_mp3(episode)
            
    def handle_stop(self, message):
        self.stop()
        
    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            self.speak_dialog('angrybeanie.stop.playing')
        

def getEpisodes(show):
    feeds = {'for science': 'http://feeds.feedburner.com/angrybeanie/ForScienceMP3?format=xml', 'women in stem': 'http://feeds.feedburner.com/WomenInStemm?format=xml'}

    feed = feedparser.parse(feeds[show])
    titles = ""
    for entry in feed.entries:
        titles += entry.title+", "

    return titles

def getLatestEpisode(show):
    feeds = {
                'for science': 'http://feeds.feedburner.com/angrybeanie/ForScienceMP3?format=xml',
                'women in stem': 'http://feeds.feedburner.com/WomenInStemm?format=xml',
                'purser explores the world': 'http://feeds.feedburner.com/PurserExploresTheWorld'
            }
    feed = feedparser.parse(feeds[show])
    entry = feed.entries[0]
    media = entry.media_content[0]['url']
    return media

def create_skill():
    return AngryBeanieSkill()
