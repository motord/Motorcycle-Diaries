# -*- coding: utf-8 -*-
# blog.models
"""
The-O-Kay-Blog models for Google App Engine

:Copyright: (c) 2009 Victor Goh <victorgoh@gmail.com>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import datetime
import aetycoon
import hashlib
import re
import logging

import blog.config as config
import blog.utils as utils

from werkzeug import Headers, Response
from werkzeug.exceptions import NotFound

HTTP_DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"

from google.appengine.ext import db
from google.appengine.ext import deferred
from google.appengine.api.labs import taskqueue

from kay.utils import (
    render_to_response, reverse,
    get_by_key_name_or_404, get_by_id_or_404,
    to_utc, to_local_timezone, url_for, raise_on_dev
)

# Create your models here.
class StaticContent(db.Model):
    body = db.BlobProperty()
    content_type = db.StringProperty(required=True)
    status = db.IntegerProperty(required=True, default=200)
    last_modified = db.DateTimeProperty(required=True, auto_now=True)
    etag = aetycoon.DerivedProperty(lambda x: hashlib.sha1(x.body).hexdigest())
    indexed = db.BooleanProperty(required=True, default=True)
    headers = db.StringListProperty()

    @classmethod
    def _get_all_paths(cls):
        """docstring for _get_all_paths"""
        keys = []
        cur = cls.all(keys_only=True).filter('indexed', True).fetch(1000)
        while len(cur) == 1000:
            keys.extend(cur)
            q.filter('indexed', True)
            q.filter('__key__ >', cur[-1])
            cur = q.fetch(1000)
        keys.extend(cur)
        return [x.name() for x in keys]

    @classmethod
    def _regenerate_sitemap(cls):
        """docstring for _regenerate_sitemap"""
        paths = cls._get_all_paths()
        rendered = utils.render_template('blog/sitemap.xml', 
                                        {'paths': paths,
                                         'config': config,
                                        })
        cls.set('/sitemap.xml', rendered, 'application/xml', False)

    @classmethod    
    def set(cls, path, body, content_type, indexed=True, **kwargs):
        """Sets the StaticContent for the provided path.

        Args:
        path: The path to store the content against.
        body: The data to serve for that path.
        content_type: The MIME type to serve the content as.
        indexed: Index this page in the sitemap?
        **kwargs: Additional arguments to be passed to the StaticContent constructor
        Returns:
        A StaticContent object.
        """
        content = cls(key_name=path,
                                body=body.encode('utf-8'),
                                content_type=content_type,
                                indexed=indexed,
                                **kwargs)
        content.put()
        try:
            now = datetime.datetime.now().replace(second=0, microsecond=0)
            eta = now.replace(second=0, microsecond=0) + datetime.timedelta(seconds=65)
            if indexed:
                deferred.defer(cls._regenerate_sitemap, 
                               _name='sitemap-%s' % (now.strftime('%Y%m%d%H%M'),),
                               _eta=eta)
        except (taskqueue.TaskAlreadyExistsError, taskqueue.TombstonedTaskError), e:
            pass
        return content   

    @classmethod
    def add(cls, path, body, content_type, **kwargs):
        def _tx():
            if cls.get_by_key_name(path):
                return None
            return cls.set(path, body, content_type, **kwargs)
        return db.run_in_transaction(_tx)

  
class BlogPost(db.Model):    
    path = db.StringProperty()
    title = db.StringProperty(required=True, indexed=False)
    body = db.TextProperty(required=True)
    #TODO:SetProperty is tied to Textarea, you can't use other widgets
    tags = aetycoon.SetProperty(basestring, indexed=False)
    published = db.DateTimeProperty()
    updated = db.DateTimeProperty(auto_now=True)
    deps = aetycoon.PickleProperty()

    @aetycoon.TransformProperty(tags)
    def normalized_tags(tags):
        return list(set(utils.slugify(x.lower()) for x in tags))

    @property
    def tag_pairs(self):
        return [(x, utils.slugify(x.lower())) for x in self.tags]

    @property
    def summary(self):
        """Returns a summary of the content"""
        match = re.search("<!--.*cut.*-->", self.body)
        if match:
            return self.body[:match.start(0)]
        else:
            return utils.truncate_html_words(self.body, config.summary_length)
    
    @property
    def hash(self):
        val = (self.title, self.body, self.tags, self.published)
        return hashlib.sha1(str(val)).hexdigest()
    
    @property
    def summary_hash(self):
        val = (self.title, self.summary, self.tags, self.published)
        return hashlib.sha1(str(val)).hexdigest()
    
    def publish(self):
        if not self.path:
            num = 0
            content = None
            while not content:
                path = utils.format_post_path(self, num)
                content = StaticContent.add(path, '', config.html_mime_type)
                num += 1
            self.path = path
            self.put()
        if not self.deps:
            self.deps = {}
        for generator_class, deps in self.get_deps():
            for dep in deps:
                if generator_class.can_defer:
                    deferred.defer(generator_class.generate_resource, None, dep)
                else:
                    generator_class.generate_resource(self, dep)
        self.put()
        
    def get_deps(self, regenerate=False):
        import blog.generators as generators
        for generator_class in generators.generator_list:
            new_deps = set(generator_class.get_resource_list(self))
            new_etag = generator_class.get_etag(self)
            old_deps, old_etag = self.deps.get(generator_class.name(), (set(), None))
            if new_etag != old_etag or regenerate:
                # If the etag has changed, regenerate everything
                to_regenerate = new_deps | old_deps
            else:
                # Otherwise just regenerate the changes
                to_regenerate = new_deps ^ old_deps
            self.deps[generator_class.name()] = (new_deps, new_etag)
            yield generator_class, to_regenerate

class VersionInfo(db.Model):
    blogokay_major = db.IntegerProperty(required=True)
    blogokay_minor = db.IntegerProperty(required=True)
    blogokay_rev = db.IntegerProperty(required=True)
    
    @property
    def blogokay_version(self):
        return (self.blogokay_major, self.blogokay_minor, self.blogokay_rev)
    