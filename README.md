# Supybot-Bible




Purpose

    Plugin for a friend to display Bible passages. Uses a simple XML api.
    Can display akjv|asv|douayrheims|kjv|web|ylt versions.

Requirements

    Working Limnoria setup on Python 2.7+

Instructions
    
    Go to your Limnoria plugin directory (usually ~/supybot/plugins) and fetch the plugin:
    
    git clone https://github.com/reticulatingspline/Supybot-Bible.git Bible
    
    This will load the plugin into your plugins directory under "Bible". Then, on IRC,
    /msg <yourbot> load Bible

Commands

    - bible [--version akjv|asv|douayrheims|kjv|web|ylt] <passage> (Ex: Job 3:14)
