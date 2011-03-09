# -*- coding: utf-8 -*-
"""
The-O-Kay-Blog configuration settings

:Copyright: (c) 2009 Victor Goh <victorgoh@gmail.com>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""
import os

blog_name = u'Motorcycle Diaries'
slogan = u'2012年上海到拉萨，行吗？'
author_name = u'赵州'

host = 'sapphire.samdeha.com'

# Themes are located in the blog/templates/themes subfolder
theme = 'motorcycle-xhtml'
post_path_format = '/%(year)d/%(month)02d/%(day)02d/%(slug)s'

# Number of posts per page in the index page
posts_per_page = 5

# Default length (in words) for post summary
summary_length = 50

# The mimetype for serving HTML files.
html_mime_type = 'text/html; charset=utf-8'

# To use disqus for commenting
use_disqus = True
disqus_forum = 'motorcyclediaries'

# To use PubSubHubbub
#hubbub_hub_url = 'http://pubsubhubbub.appspot.com'
hubbub_hub_url = 'http://pubsubhubbub.appspot.com'

# Google Site verification file name
google_site_verification = 'google0953d303961956a7.html'

# Google Analytics ID
analytics_id = 'UA-7265938-12'

# A nested list of sidebar menus, for convenience. If this isn't versatile
# enough, you can edit themes/default/base.html instead.
sidebars = [
  (u'Blogroll', [
  (u'我的链路', 'http://lian.lu/motor'),
  (u'The O-Kay-Blog Home', 'http://www.theokayblog.com'),
  (u'The Bloggart', 'http://blog.notdot.net/2009/10/Writing-a-blog-system-on-App-Engine'),
  ]),
  (u'Projects and Codes', [
  (u'The Fitness Project','http://fitness.samdeha.com/'),
  (u'GitHub Repository', 'https://github.com/motord/Motorcycle-Diaries'), 
  (u'Kay Framework','http://code.google.com/p/kay-framework/'),
  (u'Kay User Group', 'http://groups.google.com/group/kay-users?pli=1'),
  ]),
]

# Sina Weibo ID
weibo_id = '1994987653'

# Blog listing configuration
blogcatalog = ''

if 'SERVER_SOFTWARE' in os.environ and \
    os.environ['SERVER_SOFTWARE'].startswith('Dev'):
        devel = True