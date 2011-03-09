# -*- coding: utf-8 -*-
"""
The-O-Kay-Blog utility functions

:Copyright: (c) 2009 Victor Goh <victorgoh@gmail.com>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""
import re
import logging

import blog.config as config

from kay.utils import render_to_string

# Some helper methods
def slugify(s):
    from apiclient.discovery import build
    p = build("translate", "v2", developerKey="AIzaSyBw32GVmvtYlA_3JFOZ9uXmImjfC1E2KAc")
    translation = p.translations().list(
      target="en",
      q=s
    ).execute()
    s = translation['translations'][0]['translatedText']
    logging.info(s)
    return re.sub('[^a-zA-Z0-9-]+', '-', s).strip('-')

def format_post_path(post, num):
    slug = slugify(post.title)
    if num > 0:
        slug += "-" + str(num)
    return config.post_path_format % {
        'slug': slug,
        'year': post.published.year,
        'month': post.published.month,
        'day': post.published.day,
    }

def render_template(template, template_vals):
    """
    render_to_string returns a unicode string, the rendered template needs to
    be a string to be stored in BlobProperty
    """
    return render_to_string(template, template_vals)
    
def truncate_html_words(s, num):
    """
    Truncates html to a certain number of words (not counting tags and
    comments). Closes opened tags if they were correctly closed in the given
    html.
    """
    #s = force_unicode(s)
    length = int(num)
    if length <= 0:
        return u''
    html4_singlets = ('br', 'col', 'link', 'base', 'img', 'param', 'area', 'hr', 'input')
    # Set up regular expressions
    re_words = re.compile(r'&.*?;|<.*?>|(\w[\w-]*)', re.U)
    re_tag = re.compile(r'<(/)?([^ ]+?)(?: (/)| .*?)?>')
    # Count non-HTML words and keep note of open tags
    pos = 0
    ellipsis_pos = 0
    words = 0
    open_tags = []
    while words <= length:
        m = re_words.search(s, pos)
        if not m:
            # Checked through whole string
            break
        pos = m.end(0)
        if m.group(1):
            # It's an actual non-HTML word
            words += 1
            if words == length:
                ellipsis_pos = pos
            continue
        # Check for tag
        tag = re_tag.match(m.group(0))
        if not tag or ellipsis_pos:
            # Don't worry about non tags or tags after our truncate point
            continue
        closing_tag, tagname, self_closing = tag.groups()
        tagname = tagname.lower()  # Element names are always case-insensitive
        if self_closing or tagname in html4_singlets:
            pass
        elif closing_tag:
            # Check for match in open tags list
            try:
                i = open_tags.index(tagname)
            except ValueError:
                pass
            else:
                # SGML: An end tag closes, back to the matching start tag, all unclosed intervening start tags with omitted end tags
                open_tags = open_tags[i+1:]
        else:
            # Add it to the start of the open tags list
            open_tags.insert(0, tagname)
    if words <= length:
        # Don't try to close tags if we don't need to truncate
        return s
    out = s[:ellipsis_pos] + ' ...'
    # Close any tags still open
    for tag in open_tags:
        out += '</%s>' % tag
    # Return string
    return out
    
# Jinja2 Filter for datetime formatting
def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)