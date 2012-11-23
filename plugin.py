
import urllib2
import urllib
try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

class Bible(callbacks.Plugin):
    threaded = True

    # http://www.4-14.org.uk/xml-bible-web-service-api
    def bible(self, irc, msg, args, optlist, optpassage):
        """[--version akjv|asv|douayrheims|kjv|web|ylt] <passage>
        Returns text from specified Bible transation matching search parameters.
        Ex: Job 3:14, Acts 3:17-4:2, Amos 7; Psa 119:4-16, Acts 15:1-5, 10, 15
        By default, will consult KJV version. Use --version to utilize a different translation.
        """

        version = 'kjv'

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
                        irc.reply("Invalid version. Version must be one of: {0}".format(validVersions.keys()))
                        return
                    else:
                        version = value.lower()
                                            
        url = 'http://api.preachingcentral.com/bible.php?passage=' + urllib.quote(optpassage) + '&version=%s' % version

        self.log.info(url)

        try: 
            request = urllib2.Request(url, headers={"Accept" : "application/xml"})
            u = urllib2.urlopen(request)
        except:
            irc.reply("Failed to load url: %s" % url)
            return
        
        # now try to process XML.
        try:
            tree = ElementTree.parse(u)
            document = tree.getroot()
        except:
            irc.reply("Failed to parse XML. Check logs.")
            return
        
        # first check for when syntax is broke. They don't give a proper error message.
        # Error return: ParseError: mismatched tag: line 1909, column 2
        if document.find('range/result') is None or document.tag != 'bible':
            irc.reply("ERROR: Failed to load/parse the verse or page. Check your syntax. ")
            return
        
        # if you do give an invalid passage, it will spit out an error in XML. 
        if document.find('range/error') is not None:
            irc.reply("ERROR: '{0}' when searching for: {1}".format(document.find('range/error').text, optpassage))
            return
        
        for node in document.findall('range/item'):
            bookname = node.find('bookname')
            chapter = node.find('chapter')
            verse = node.find('verse') 
            text = node.find('text')
            irc.reply("[{0}] {1} {2}:{3} :: {4}".format(ircutils.mircColor(version.upper(), 'red'), ircutils.bold(bookname.text),\
                ircutils.bold(chapter.text), ircutils.bold(verse.text), text.text))
            
    bible = wrap(bible, [getopts({'version':('text')}), ('text')])

 


Class = Bible
