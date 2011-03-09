"""
The-O-Kay-Blog views to handle static content

:Copyright: (c) 2009 Victor Goh <victorgoh@gmail.com>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""
import logging
import datetime

from werkzeug import Headers, Response, redirect
from werkzeug.exceptions import NotFound
from kay.utils import render_to_response
import blog.config as config
from blog.models import StaticContent

HTTP_DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"

def _output(content, serve=True):
    """Output the content in the datastore as a HTTP Response"""
    headers = Headers()
    if content.content_type:
        headers['Content-Type'] = content.content_type
    last_modified = content.last_modified.strftime(HTTP_DATE_FMT)
    headers.add('Last-Modified', last_modified)
    headers.add('ETag', '"%s"' % (content.etag,))
    for header in content.headers:
        key, value = header.split(':', 1)
        headers[key] = value.strip()
    if serve:
        response = Response(content.body, content_type=content.content_type,
                    headers=headers, status=content.status)
    else:
        response = Response(status=304)
    return response
        
def get_content(request, path=''):
    """Get content from datastore as requested on the url path
    
    Args:
        path - comes without leading slash. / added in code
    
    """
    content = StaticContent.get_by_key_name("/%s" % path)
    if not content:
        if path == '':
            # Nothing generated yet. Inform user to create some content
            return render_to_response("blog/themes/%s/listing.html" % config.theme, 
                                {'config': config, 'no_post': True,})
        else:
            raise NotFound
    
    serve = True
    # check modifications and etag
    if 'If-Modified-Since' in request.headers:
        last_seen = datetime.datetime.strptime(
            request.headers['If-Modified-Since'], HTTP_DATE_FMT)
        if last_seen >= content.last_modified.replace(microsecond=0):
            serve = False
    if 'If-None-Match' in request.headers:
        etags = [x.strip('" ')
                 for x in request.headers['If-None-Match'].split(',')]
        if content.etag in etags:
            serve = False
    response = _output(content, serve)
    return response