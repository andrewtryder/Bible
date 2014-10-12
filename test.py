###
# Copyright (c) 2012-2014, spline
# All rights reserved.
#

###

from supybot.test import *

class BibleTestCase(PluginTestCase):
    plugins = ('Bible',)
    
    def testBible(self):
        self.assertRegexp('bible --version kjv Job 3:14', 'With kings and counsellers of the earth, which built desolate places for themselves')
        self.assertRegexp('bible --version kjv web 3:15', 'or with princes who had gold, who filled their houses with silver')


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
