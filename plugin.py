###
# Copyright (c) 2012-2013, spline
# All rights reserved.
#

###
# my libs
try:  # use cElementTree but revert back to regular ET
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree
# supybot libs
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring

_ = PluginInternationalization('UrbanDictionary')

class Bible(callbacks.Plugin):
    threaded = True

    # http://www.4-14.org.uk/xml-bible-web-service-api
    def bible(self, irc, msg, args, optlist, optpassage):
        """[--version akjv|asv|douayrheims|kjv|web|ylt] <passage>
        Returns text from specified Bible transation matching search parameters.
        Ex: Job 3:14, Acts 3:17-4:2, Amos 7; Psa 119:4-16, Acts 15:1-5, 10, 15
        By default, will consult KJV version. Use --version to utilize a different translation.
        """

        # set default version
        version = 'kjv'
        # check optlist (getopts)
        validVersions = {'akjv':'American King James Version',
                         'asv':'American Standard Version',
                         'douayrheims':'Douay-Rheims',
                         'kjv':'King James Version',
                         'web':'World English Bible',
                         'ylt':'Youngs Literal Translation' }

        if optlist:
            for (key, value) in optlist:
                if key == 'version':
                    if value.lower() not in validVersions:
                        irc.reply("ERROR: Invalid version. Version must be one of: {0}".format(validVersions.keys()))
                        return
                    else:
                        version = value.lower()
        # build and fetch url.
        url = 'http://api.preachingcentral.com/bible.php?passage='
        url += utils.web.urlquote(optpassage) + '&version=%s' % version
        try:
            u = utils.web.getUrl(url)
        except utils.web.Error as e:
            self.log.error("ERROR opening {0} message: {1}".format(url, e))
            irc.reply("ERROR: could not open {0} message: {1}".format(url, e))
            return
        # now try to process XML.
        try:
            document = ElementTree.fromstring(u)
        except Exception, e:
            irc.reply("ERROR: Failed to parse XML. Check logs.")
            self.log.error("ERROR: {0} Could not parse Bible XML. {1}".format(e, u))
            return
        # first check for when syntax is broke. They don't give a proper error message.
        # Error return: ParseError: mismatched tag: line 1909, column 2
        if document.find('range/result') is None or document.tag != 'bible':
            irc.reply("ERROR: Failed to load/parse the verse or page. Check your syntax.")
            return
        # if you do give an invalid passage, it will spit out an error in XML.
        if document.find('range/error'):
            irc.reply("ERROR: '{0}' when searching for: {1}".format(document.find('range/error').text, optpassage))
            return
        # prepare output. limit to 5 lines before stopping for flood.
        founditems = document.findall('range/item')
        # now iterate over these.
        for i, node in enumerate(founditems):
            bookname = node.find('bookname')
            chapter = node.find('chapter')
            verse = node.find('verse')
            text = node.find('text')
            if i < 5:
                irc.reply("[{0}] {1} {2}:{3} :: {4}".format(ircutils.mircColor(version.upper(), 'red'),\
                                                        ircutils.bold(bookname.text),\
                                                        ircutils.bold(chapter.text),\
                                                        ircutils.bold(verse.text),\
                                                        text.text))
            else:
                irc.reply("ERROR: I have more than 5 matching passages from your query ({0} left). Please be more specific.".format(len(founditems)-5))
                break

    bible = wrap(bible, [getopts({'version':('text')}), ('text')])

Class = Bible
