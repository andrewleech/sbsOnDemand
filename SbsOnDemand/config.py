## @namespace SbsOnDemand::config
# Module for setting configuration variables and storing global constants such as urls

# User-specified constants

## Manual proxy specification (can be used for debugging)
#
# Set to None for default (system) proxy
#
# Should be a dict object, such as {'http': '127.0.0.1:8080'}
PROXY = None

# Constants - don't change
API_BASE = "http://www.sbs.com.au/api/video_feed"
#MENU_URI = "http://www.sbs.com.au/ondemand/js/video-menu" # It's gone now (2015/08/01)
LOGIN_URI = "http://my.sbs.com.au/go/login/onesiteSignIn"
LOGOUT_URI = "http://www.sbs.com.au/api/Member/logout"

SEARCH_PREFIX = "http://www.sbs.com.au/api/video_search/v2/"
SITENAV_URI = "http://www.sbs.com.au/ondemandcms/sitenav"

ONDEMAND_UI_BASE_URI = "http://www.sbs.com.au/ondemand/video/"
ONDEMAND_UI_FULLSCREEN_URI = "http://www.sbs.com.au/ondemand/video/single/"

RELEASE_URL_KEY = 'http://resources.sbs.com.au/vod/theplatform/core/current/swf/flvPlayer.swf?releaseUrl'
VALID_URL_SUFFIX = '.csmil/bitrate=0?v=2.9.4&fp=MAC%2011,5,502,136&r=XBQYK&g=FSCQTSPZYLLE'
ONDEMAND_UI_VIDEO_CSS_QUERY = 'meta[property="og:video"]'
#MPX_FEEDID = "dYtmxB"
MPX_FEEDID = "Bgtm9B"
# SEARCH_FEEDID = "search"
ALLDATA_FEEDID = "CxeOeDELXKEv"
SINGLE_FEED_PREFIX = 'http://feed.theplatform.com/f/Bgtm9B/sbs-section-programs/'

DEFAULT_FEEDS = [
    {"name": "Programs", "feedId": "section-programs"},
    {"name": "Clips", "feedId": "section-clips"},
    {"name": "Events", "feedId": "section-events"},
    {"name": "Last Chance", "feedId":"videos-lastchance"},
    {"name": "Featured Programs", "feedId":"featured-programs-prod"},
    {"name": "Documentary", "url": 'http://www.sbs.com.au/api/video_feed/f/Bgtm9B/sbs-section-sbstv?form=json&byCategories=Documentary|Factual|Factual%2FAnimation|Factual%2FArchaeology|Factual%2FBiography|Factual%2FBusiness+and+Economics|Factual%2FCulture+and+Society|Factual%2FDocu-drama|Factual%2FHealth+%2B+Science+and+Technology|Factual%2FHistory|Factual%2FLifestyle|Factual%2FPolitics+and+Current+Affairs|Factual%2FNature+and+Environment|Factual%2FSport|Factual%2FSexuality%2CSection%2FClips|Section%2FPrograms&count=true&defaultThumbnailAssetType=Thumbnail'},
    {"name": "Featured Clips", "feedId":"featured-clips"}
]

## Not sure how to use this one
# http://www.sbs.com.au/api/video_feed/f/Bgtm9B/sbs-xbox-search

MENU = [
    # TODO Featured comes up double menu

    ("Programs"  , { "menu": [
        ("Featured"  , {"feedId": 'sbs-featured-programs-prod', "filter": {"byCategories": "!Film"}}), # "url": "http://www.sbs.com.au/api/video_feed/f/Bgtm9B/sbs-featured-programs-prod?form=json&count=true&sort=pubDate%7Casc&byCategories=!Film"}),
        #("A - Z"   , { "url": ""}),
        ("Last Chance" , { "feedId": 'sbs-video-lastchance', "filter": {"byCategories": "Section%2FPrograms,Drama%7CComedy%7CDocumentary%7CArts%7CEntertainment%7CFood%7CFactual%7CMovies"}}), #"url": "http://www.sbs.com.au/api/video_feed/f/Bgtm9B/sbs-video-lastchance?form=json&count=true&byCategories=Section%2FPrograms,Drama%7CComedy%7CDocumentary%7CArts%7CEntertainment%7CFood%7CFactual%7CMovies&sort=expirationDate%7Casc"}),
        ("Popular" , { "sitenav": "Programs/groups/Popular"}),
        ("Genres" , { "sitenav": "Programs/groups/Genres"}),
    ]}),
    ("Movies"    , { "menu": [
        ("Featured"  , { "feedId": 'sbs-featured-programs-prod', "filter": {"byCategories": "Film"}}), # "url": "http://www.sbs.com.au/api/video_feed/f/Bgtm9B/sbs-featured-programs-prod?form=json&count=true&sort=pubDate%7Casc&byCategories=Film"}),
        ("Collections" , { "sitenav": "Movies/groups/Collections"}),
        ("Genres" , { "sitenav": "Movies/groups/Genres"}),
    ]}),

    # TODO fill out below

    ("Channels"  , { "menu": [
        ("SBS",                    { "url": "" }),
        ("SBS TWO",                { "url": "" }),
        ("NITV",                   { "url": "" }),
        ("World Movies",           { "url": "" }),
        ("On Demand Exclusives",   { "url": "" }),
    ]}),
    ("News"      , { "url": "" }),
    ("Sport"     , { "url": "" }),
]