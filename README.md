Supybot-Bible
=============

Purpose

    Plugin for a friend to display Bible passages. Uses a simple XML api.
    Can display akjv|asv|douayrheims|kjv|web|ylt versions.

Instructions
    
    Should work fine on an up-to-date supybot/Limnoria install. I develop on python 2.7.3 but a 2.6+
    install should be fine. The module uses the built-in ElementTree module.
    Just grab the plugin, load it, and you should be good to go.
    
Commands

    - bible [--version akjv|asv|douayrheims|kjv|web|ylt] <passage> (Ex: Job 3:14)
