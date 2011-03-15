# -*- coding: utf-8 -*-
"""
The-O-Kay-Blog post deployment tasks

:Copyright: (c) 2009 Victor Goh <victorgoh@gmail.com>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""
import logging
import os
import datetime

from google.appengine.api.labs import taskqueue
from google.appengine.ext import deferred

import blog.config as config
import blog.utils as utils
from blog.models import VersionInfo, BlogPost, StaticContent

BLOGOKAY_VERSION = (1, 0, 1)

def regenerate(batch_size=50, seen=None, start_ts=None):
    """Regenerate all static content"""
    if not seen:
        seen = set()
    q = BlogPost.all().order('-published')
    q.filter('published <', start_ts or datetime.datetime.max)
    posts = q.fetch(batch_size)
    for post in posts:
        for generator_class, deps in post.get_deps(True):
            for dep in deps:
                if (generator_class.__name__, dep) not in seen:
                    logging.warn((generator_class.__name__, dep))
                    seen.add((generator_class.__name__, dep))
                    deferred.defer(generator_class.generate_resource, None, dep)
        post.put()
    if len(posts) == batch_size:
        deferred.defer(regenerate, batch_size, seen, posts[-1].published)


def generate_static_pages(pages):
    def generate(previous_version):
        for path, template, indexed in pages:
            rendered = utils.render_template(template, {'config':config})
            StaticContent.set(path, rendered, config.html_mime_type, indexed)
    return generate

post_deploy_tasks = []
post_deploy_tasks.append(generate_static_pages([
    ('/search', 'blog/themes/%s/search.html' % config.theme, True),
    ('/cse.xml', 'blog/cse.xml', False),
    ('/robots.txt', 'blog/robots.txt', False),
    ('/cloudsave2vdisk/update.xml', 'blog/cloudsave2vdisk_update.xml', True),
    ])) 

       
def regenerate_all(previous_version):
    """Regenerate all static content after checking"""
    if previous_version < BLOGOKAY_VERSION:
        deferred.defer(regenerate)

post_deploy_tasks.append(regenerate_all)

        
def site_verification(previous_version):
    StaticContent.set('/' + config.google_site_verification,
                      utils.render_template('blog/site_verification.html',
                                            {'config':config}),
                      config.html_mime_type, False)

if config.google_site_verification:
    post_deploy_tasks.append(site_verification)

            
def run_deploy_task():
    """Attempts to run the per-version deploy task."""
    task_name = 'deploy-%s' % os.environ['CURRENT_VERSION_ID'].replace('.','-')
    try:
        deferred.defer(try_post_deploy, _name=task_name, _countdown=10)
    except (taskqueue.TaskAlreadyExistsError, taskqueue.TombstonedTaskError), e:
        pass
        
def try_post_deploy():
    """Runs post_deploy() iff it has not been run for this version yet."""
    version_info = VersionInfo.get_by_key_name(
        os.environ['CURRENT_VERSION_ID'])
    if not version_info:
        q = VersionInfo.all()
        q.order('-blogokay_major')
        q.order('-blogokay_minor')
        q.order('-blogokay_rev')
        post_deploy(q.get())
        
def post_deploy(previous_version):
    """Carries out post-deploy functions, such as rendering static pages."""
    for task in post_deploy_tasks:
        logging.info(task)
        task(previous_version)
        
    new_version = VersionInfo(
        key_name=os.environ['CURRENT_VERSION_ID'],
        blogokay_major = BLOGOKAY_VERSION[0],
        blogokay_minor = BLOGOKAY_VERSION[1],
        blogokay_rev = BLOGOKAY_VERSION[2])
    new_version.put()


