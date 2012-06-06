import re
import urllib
import urllib2
import json

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

# http://www.4-14.org.uk/xml-bible-web-service-api
# def bible(book, chapter, verse):
#    url = "http://api.preachingcentral.com/bible.php?passage=%s%s:%s&version=asv" % (book, chapter, verse)
#    parsed = lxml.html.fromstring(urllib2.urlopen(url).read())
#    b = parsed.find('range').find('item').find('bookname').text_content()
#    c = parsed.find('range').find('item').find('chapter').text_content()
#    v = parsed.find('range').find('item').find('verse').text_content() 
#    t = parsed.find('range').find('item').find('text').text_content() 
#    return "<{C4}{B}%s %s:%s{}: {B}%s{}>" % (b, c, v, t)

class Bible( callbacks.Plugin ):
    threaded = True

    def bible(self, irc, msg, args, translation, search):
      """<translation> <search>
      Returns text from specified Bible transation matching search parameters.
      Ex: kjv Job 3:14
      """

      translation = translation.upper()
      url = 'http://mobile.biblegateway.com/passage/?search=' + urllib.quote( search ) + '&version=' + translation

      # test the request/connection
      try: 
        req = urllib2.Request(url)
        stream = urllib2.urlopen(req)
        html = stream.read()
      except urllib2.HTTPError, err:
        irc.reply("Failed to load request")
        self.log.warning("Failed to load request: %s" % err.code)

      # test for content
      _biblegatewayre = re.compile( r'div class="result-text-style-normal text-html ">\s(.*?)</div>', re.S | re.I)
      m = _biblegatewayre.search( html )

      if m:
        title = re.search(r'.*meta.*title.*content="(.*?)"', html).group(1)
        title = re.sub(r'Bible Gateway passage: ', '', title)

        #verse = re.search(r'(.*?)-', title).group(1)
        #fullversion = re.search(r'- (.*?)', title).group(1)
        #self.log.info(fullversion)
        #irc.reply(search)
        #irc.reply(translation)

        # description as well
        description = re.search(r'.*meta.*description.*content="(.*?)"', html).group(1)

        irc.reply(title)
        irc.reply(description)
      
      elif '>0 Results' in html or 'No results found' in html:
          irc.reply( 'No results found for %s.' % search )
      else:
          irc.error( 'Source page has changed formatting.  Plugin update required.' )
    bible = wrap( bible, [ 'something', 'text' ] )

    def votd(self, irc, msg, args):
      """
      Returns the verse of the day from biblegateway.com
      """

      url = 'http://mobile.biblegateway.com/votd/get/?format=json&version=KJV'
      response = urllib.urlopen(url)
      json_response = response.read()
      response_obj = json.loads(json_response)

      text = response_obj['votd']['text']
      text = re.sub('&[rl]dquo;', '"', text)
      display_ref = response_obj['votd']['display_ref']
      version_id = response_obj['votd']['version_id']

      output = text + " (" + ircutils.bold(ircutils.underline(display_ref)) + " (" + version_id + "))"

      irc.reply(output)

    votd = wrap(votd)


Class = Bible
