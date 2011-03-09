# -*- coding: utf-8 -*-
# blog.urls
"""
The-O-Kay-Blog routing configuration

:Copyright: (c) 2009 Victor Goh <victorgoh@gmail.com>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""
from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)

import blog.views.admin
import blog.views.static

blog.post_deploy.run_deploy_task()

def make_rules():
    return [
        EndpointPrefix('blog/', [
            Rule('/', endpoint='get_content'),
            Rule('/admin/', endpoint='admin'),
            Rule('/admin/<int:start>/<int:count>', endpoint='admin'),
            Rule('/admin/post/<int:post_id>', endpoint='post'),
            Rule('/admin/newpost', endpoint='newpost'),
            Rule('/admin/regenerate', endpoint='regenerate'),
            Rule('/<path:path>', endpoint='get_content'),
            ]),
    ]

all_views = {
    'blog/admin': blog.views.admin.index,
    'blog/post' : blog.views.admin.post,
    'blog/newpost': blog.views.admin.post,
    'blog/regenerate': blog.views.admin.regenerate_site,
    'blog/get_content': blog.views.static.get_content,
}
