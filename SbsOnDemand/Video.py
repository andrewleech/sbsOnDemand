## @namespace SbsOnDemand::Video
# Module for managing videos

import re
try:
    import simplejson as json
except ImportError: 
    import json
import urllib, urlparse
import config
import xml.etree.ElementTree as xml
from Category import Category
from Media import Media

## This exception is raised when a method is invoked on a Video object that requires an ID
class NoIDException(Exception):
    def __str__(self):
        return "No ID Specified"

## Gets a video from its id
# @param videoId the ID number of the video
# @return a Video object
def getVideo(videoId):
    video = Video({"id":videoId})
    video._updateVideo()
    return video

## Represents a single video
class Video(object):

    ## Creates a video object
    # @param params the video data to be parsed
    def __init__(self,params):
        self._parseVideo(params)
        
    ## Parses video data and populates Video data members
    # @param params the video data to be parsed
    def _parseVideo(self,params):
        videoId = params.get('id',None)
        if videoId is not None and videoId.isdigit():
            self.id = str(videoId)
        elif videoId is not None:
            self.id = re.search("\d+",videoId).group(0)
        else:
            self.id = None
        self.url = None
        self.title = params.get('title',None)
        self.description = params.get('description',None)
        self.thumbnail = params.get('plmedia$defaultThumbnailUrl',None)
        self.episodeNumber = params.get('pl1$episodeNumber',None)
        self.availableDate = params.get('media$availableDate',None)
        self.expirationDate = params.get('media$expirationDate',None)
        self.programName = params.get('pl1$programName',None)
        keywords = params.get('media$keywords',None)
        if keywords is not None:
            self.keywords = keywords.split(",")
        else:
            self.keywords = None
        self.pubDate = params.get('pubDate',None)
        self.categories = []
        for category in params.get('media$categories',[]):
            self.categories.append(Category(category))
        self.duration = None
        self._media = {}
        self._media['content'] = []
        self._media['thumbnails'] = []
        self._mediaHasUrl = True
        rtmpSecured = False
        mediaContent = params.get('media$content',[])
        for media in mediaContent:
            x=media.get('plfile$assetTypes',[])
            if (len(x) > 0 and x[0][:4] == "RTMP"):
                rtmpSecured = True
        if rtmpSecured:
            #Parse web page and make Media objects from SMIL instead
            opener = urllib.FancyURLopener(config.PROXY)
            smil_uri = ''
            fullurl = "{0}{1}".format(config.ONDEMAND_UI_BASE_URI,self.id)
            f = opener.open(fullurl)
            og_video = re.findall('<.*?og:video.*?>', f.read())
            if (len(og_video) < 1):
                print "Can't find the video part on the webpage.  HELP!"
                pass #Need to complain loudly
            else:
                m = re.search('content="(.+?)"', og_video[0])
                videourl = m.group(1)
                p = urlparse.parse_qs(videourl)
                smil_uri = p.get(config.RELEASE_URL_KEY,[''])[0]
                if (smil_uri != ''):
                    smil_uri += "&format=smil"
            if len(smil_uri) > 0:
                f = opener.open(smil_uri)
                smil_content = f.read()
                self.url = self._watchableUrlFromSmil(smil_content)
                print self.url
        else:
            for media in mediaContent:
                mediaObj = Media(media)
                self._media['content'].append(mediaObj)
                if mediaObj.url is None:
                    self._mediaHasUrl = False
                if self.duration is None and mediaObj.duration is not None:
                    self.duration = mediaObj.duration
        mediaThumbnails = params.get('media$thumbnails',[])
        for media in mediaThumbnails:
            mediaObj = Media(media)
            self._media['thumbnails'].append(mediaObj)
            if mediaObj.url is None:
                self._mediaHasUrl = False
                
    ## Get the associated videos from smil file
    def _watchableUrlFromSmil(self, smil_content):
        videos = re.findall('<video.*?src="(.+?akamai.+?)".*?>', smil_content)
        videos.reverse()
        for video in videos:
            match = re.search('(\d+)K.mp4', video)
            bitrate = match.group(1)
            url = re.sub('(\d+)K.mp4', r',\1,K.mp4', video)
            return url + config.VALID_URL_SUFFIX
        return ''

    ## Downloads the video data, allowing it to be parsed
    def _updateVideo(self):
        url = config.API_BASE + '/f/' + config.MPX_FEEDID + '/' + config.ALLDATA_FEEDID + '/' + self.id + '?' + urllib.urlencode({"form":"json"})
        page = urllib.urlopen(url)
        data = json.load(page)
        self._parseVideo(data)
        
    ## Gets the available media associated with the video
    # @param withUrl whether to ensure that the media has a download url
    # @return a dict with two keys, `content` and `thumbnails`, each containing an array of Media objects 
    def getMedia(self, withUrl = True):
        if self.id is None:
            raise NoIDException()
        if not self._mediaHasUrl and withUrl:
            self._updateVideo()
            return self._media
        else:
            return self._media
    
    ## @see getMedia
    media = property(getMedia)
    
