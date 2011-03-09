# -*- coding: utf-8 -*-
"""
The-O-Kay-Blog Generators to create content using GAE Task queue

:Copyright: (c) 2009 Victor Goh <victorgoh@gmail.com>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import hashlib
import logging
import urllib
import itertools
import datetime

from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext import deferred

import blog.config as config
import blog.utils as utils
from blog.models import StaticContent


generator_list = []

class ContentGenerator(object):
    """A class that generates content and dependency list for blog posts"""
    can_defer = True
    
    @classmethod
    def name(cls):
        return cls.__name__
        
    @classmethod
    def get_resource_list(cls, post):
        raise NotImplementedError()
        
    @classmethod
    def get_etag(cls, post):
        raise NotImplementedError()
    
    @classmethod
    def generate_resource(cls, post, resource):
        raise NotImplementedError()
        
class PostContentGenerator(ContentGenerator):
    """ContentGenerator the individual blog posts."""
    can_defer = False
    
    @classmethod
    def get_resource_list(cls, post):
        return [post.key().id()]
        
    @classmethod
    def get_etag(cls, post):
        return post.hash
        
    @classmethod
    def generate_resource(cls, post, resource):
        from blog.models import BlogPost
        if not post:
            post = BlogPost.get_by_id(resource)
        else:
            assert resource == post.key().id()
        template_vals = {
            'post': post,
            'config': config,
        }
        template_name = "blog/themes/%s/post.html" % config.theme
        rendered = utils.render_template(template_name, template_vals)
        StaticContent.set(post.path, rendered, config.html_mime_type)
generator_list.append(PostContentGenerator)

class ListingContentGenerator(ContentGenerator):
    path = None
    """THe path for listing pages."""
    
    first_page_path = None
    """The path for the first listing page."""
    
    @classmethod
    def _filter_query(cls, resource, q):
        """Applies filters to the BlogPost query.
        
        Args:
            resource: The resource being generated
            q: The query to act upon
        
        """
        pass
        
    @classmethod
    def get_etag(cls, post):
        return post.summary_hash
        
    @classmethod
    def generate_resource(cls, post, resource, pagenum=1, start_ts=None):
        from blog.models import BlogPost
        q = BlogPost.all().order('-published')
        q.filter('published <', start_ts or datetime.datetime.max)
        cls._filter_query(resource, q)

        posts = q.fetch(config.posts_per_page + 1)
        more_posts = len(posts) > config.posts_per_page

        path_args = {
            'resource': resource,
        }
        path_args['pagenum'] = pagenum - 1
        prev_page = cls.path % path_args
        path_args['pagenum'] = pagenum + 1
        next_page = cls.path % path_args
        template_vals = {
            'posts': posts[:config.posts_per_page],
            'prev_page': prev_page if pagenum > 1 else None,
            'next_page': next_page if more_posts else None,
            'config': config,
        }
        template_name = "blog/themes/%s/listing.html" % config.theme
        rendered = utils.render_template(template_name, template_vals)
        
        path_args['pagenum'] = pagenum
        StaticContent.set(cls.path % path_args, rendered, config.html_mime_type)

        if pagenum == 1:
            StaticContent.set(cls.first_page_path % path_args, rendered, config.html_mime_type)
        if more_posts:
            deferred.defer(cls.generate_resource, None, resource, pagenum + 1,
                           posts[-2].published)

class IndexContentGenerator(ListingContentGenerator):
    """ContentGenerator for the homepage of the blog and archive pages."""
    path = '/page/%(pagenum)d'
    first_page_path = '/'
    
    @classmethod
    def get_resource_list(cls, post):
        return [u"index"]
generator_list.append(IndexContentGenerator)

class TagContentGenerator(ListingContentGenerator):
    """ContentGenerator for the tags pages."""
    path = '/tag/%(resource)s/%(pagenum)d'
    first_page_path = '/tag/%(resource)s'
    
    @classmethod
    def get_resource_list(cls, post):
        return post.normalized_tags

    @classmethod
    def _filter_query(cls, resource, q):
        q.filter('normalized_tags =', resource)
generator_list.append(TagContentGenerator)

class AtomContentGenerator(ContentGenerator):
    """ContentGenerator for Atom Feeds."""
    
    @classmethod
    def get_resource_list(cls, post):
        return [u"atom"]
        
    @classmethod
    def get_etag(cls, post):
        return post.hash

    @classmethod
    def generate_resource(cls, post, resource):
        from blog.models import BlogPost
        q = BlogPost.all().order('-updated')
        posts = list(itertools.islice((x for x in q if x.path), 10))
        for post in posts:
            updated = post.updated
            break
        template_vals = {
            'posts': posts,
            'config': config,
            'updated': updated,
        }
        rendered = utils.render_template("blog/atom.xml", template_vals)
        StaticContent.set('/feeds/atom.xml', rendered,
                          'application/atom+xml; charset=utf-8')
        if config.hubbub_hub_url:
            cls.send_hubbub_ping(config.hubbub_hub_url)

    @classmethod
    def send_hubbub_ping(cls, hub_url):
        data = urllib.urlencode({
            'hub.url': 'http://%s/feeds/atom.xml' % (config.host,),
            'hub.mode': 'publish',
        })
        response = urlfetch.fetch(hub_url, data, urlfetch.POST)
        if response.status_code / 100 != 2:
            raise Exception("Hub ping failed", response.status_code, response.content)
generator_list.append(AtomContentGenerator)

        