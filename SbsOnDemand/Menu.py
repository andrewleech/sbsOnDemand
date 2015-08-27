## @namespace SbsOnDemand::Category
# Module for managing menus

try:
    import simplejson as json
except ImportError:
    import json
try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs
import urllib

import config

## Represents a Menu
class Menu(object):
    '''

    '''

    ## @var path
    # the current position in the menu structure
    ## @var name
    # the heading of the current menu
    ## @var children
    # the items in the current menu

    ## Creates a Category object
    # @param params Dictionary of parameters, should include `media$name` and `media$scheme`
    def __init__(self, path="", name="SBS On Demand"):
        self.path = path
        self.name = name
        self.children = {}
        self._sitenav = None

    def _getSitenav(self):
        if not self._sitenav:
            assert isinstance(config.SITENAV_URI, basestring)

            page = urllib.urlopen(config.SITENAV_URI)
            page_source = page.read()
            sitenav = json.loads(page_source)
            self._sitenav = sitenav.get('sitenav', None)
        return self._sitenav


    def _parseSitenav(self, sitenav_path):
        menu = []
        elements = self._getSitenav()
        branch = ""
        prev_branch = ""
        # print sitenav_path
        # print elements
        # print ""
        if elements:
            tree = sitenav_path.split('/')
            for branch in tree:
                # print "branch="+str(branch)
                # print elements
                # print ""
                if isinstance(elements, list):
                    for element in elements:
                        if branch == element.get('title'):
                            elements = element
                elif isinstance(elements, dict):
                    if branch in elements:
                        elements = elements[branch]

            # check if elements is genre / poular and parse accordingly.
            if tree[-1] == "Genres":
                for row in elements['children']:
                    name = row['title']
                    menu.append((name,Menu(path='/'.join((self.path, name)),
                                         name=name)))
            elif tree[-2] == "Genres":
                from Feed import Feed

                # from Category import Category
                name = tree[-1]

                # The sitemap doesn't always match the byCategory filters :-(
                genremap = {
                    "Culture & Society"     : "Factual/Culture and Society",
                    "Nature & Environment"  : "Factual/Nature and Environment",
                    "News & Current Affairs": "News and Current Affairs",
                    "Feature Documentaries" : "Documentary Feature",
                    "Mystery & Crime"       : "Mystery Crime",
                    "History"               : "Factual/History",
                    "Health, Science & Technology" : "Factual/Health + Science and Technology",
                }
                name = genremap.get(name, name) # take mapped name if it has mapping
                category = 'Film/'+name if 'Movies' in tree else name
                filt = { 'byCategories':category,
                         # 'byCustomValue':"{useType}{Full%20Episode}"
                         }

                if name in [
                    "Culture & Society"    ,
                    "Feature Documentaries",
                    "Mystery & Crime"      ,
                    "Nature & Environment" ,
                    "History",
                    "Health, Science & Technology",
                ]:
                    feedid = 'sbs-section-sbstv'
                    # filt["byCustomValue"] = "{useType}{Full%20Episode}"
                else:
                    feedid = 'sbs-section-programs'

                # menu = (name,Category({'media$name':category}).getFeed(feedid))
                menu = (name, Feed({'feedId':feedid, 'filter':filt}))

            elif tree[-1] == "Popular":
                for row in elements['children']:
                    name = row['title']
                    menu.append((name,Menu(path='/'.join((self.path, name)),
                                         name=name)))
            elif tree[-2] == "Popular":
                import Feed
                name = tree[-1]
                ## TODO: find a better way to parse popular href/title into a feed url
                ## without needing to run the js on each sbs website
                ## # ( in http://www.sbs.com.au/ondemand/app.concat.js )
                menu = (name,Feed.searchFeed(query=name))


        # from pprint import pprint
        # print ""
        # pprint(elements)
        # pprint(menu)
        return menu

    ## Gets current menu
    def getMenu(self):
        menu = []
        if not self.path:
            for name, details in config.MENU:
                menu.append((name,Menu(path=name,
                                 name=name)))
        else:
            menu_dict = dict(config.MENU)
            # tree = os.path.split(self.path)
            tree = self.path.split('/')
            # tree = urlparse.urlparse(self.path)
            branch = ""
            child = {}
            idx = 0
            for idx in range(len(tree)):
                branch = tree[idx]
                child = menu_dict[branch]
                if 'menu' in child:
                    menu_dict = dict(child['menu'])
                else:
                    break
            if 'menu' in child:
                for name, details in child['menu']:
                    menu.append((name,Menu(path='/'.join((self.path, name)),
                                     name=name)))
            elif 'sitenav' in child:
                menu = self._parseSitenav('/'.join([child['sitenav']] + tree[idx+1:]))

            elif 'feedId' in child:
                import Feed
                menu = [(branch, Feed.Feed(child))]

        return menu

if __name__ == "__main__":
    from pprint import pprint
    menu = Menu().getMenu()
    menu2 = menu[0].getMenu()
    menu3 = menu2[3].getMenu()

    pprint(Menu().getMenu())