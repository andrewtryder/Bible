###
# Copyright (c) 2012-2014, spline
# All rights reserved.
#

###

import supybot.conf as conf
import supybot.registry as registry

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Bible', True)


Bible = conf.registerPlugin('Bible')
# This is where your configuration variables (if any) should go.  For example:
conf.registerChannelValue(Bible, 'disableANSI', registry.Boolean(False, """Disable ANSI output in channel?"""))


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
