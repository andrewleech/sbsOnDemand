#!/usr/bin/env python
# Initial version http://delx.net.au/hg/jamesstuff/rev/706a749fc341
# Changes by Michael van der Kolff <mvanderkolff@gmail.com>
import sys
sys.path.append('../')

import SbsOnDemand.Feed

programs = SbsOnDemand.Feed.getFeedFromId('section-programs')
print programs.getVideos()
