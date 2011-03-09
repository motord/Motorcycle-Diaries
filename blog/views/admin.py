"""
The-O-Kay-Blog Admin views

:Copyright: (c) 2009 Victor Goh <victorgoh@gmail.com>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""
import logging
import datetime

from kay.auth.decorators import admin_required
from kay.utils import render_to_response
from google.appengine.ext import deferred

import blog.config as config
from blog.forms import PostForm
from blog.models import BlogPost

from blog.post_deploy import regenerate, post_deploy, BLOGOKAY_VERSION

def with_post(fun):
    """ Decorator to retrieve a blog post if a post_id is provided """
    def decorate(self, post_id=None):
        post = None
        if post_id:
            post = BlogPost.get_by_id(int(post_id))
            if not post:
                raise NotFound
        return fun(self, post)
    return decorate

@admin_required                        
@with_post
def post(request, post):
    """ Create and edit Blog Posts 
    
    Args
        post: Blog post that is being edited
    
    GET Method
    Display an empty form when adding a new post. 
    Display a filled in form when editing an existing post.
    
    POST Method
    When submiting an existing post or creating a new post. 
    
    """
    form = PostForm(instance=post,
                    initial={'draft': post and post.published == datetime.datetime.max})

    edit = post != None
    if request.method == 'POST':
        if form.validate(request.form):
            post = form.save()
            if form.data['draft']:
                post.published= datetime.datetime.max
                post.put()
            else:
                if not post.path:
                    post.published = datetime.datetime.now()
                post.publish()
            return render_to_response("blog/admin/published.html", 
                                     {'config': config, 'post':post,
                                      'draft': form.data['draft'],
                                      'edit': edit,} )

    template_vals = {'config': config,
                     'form': form.as_widget(),
                     'edit': edit,
                     'menu_new': not edit, }        
    return render_to_response('blog/admin/edit.html',  
                             template_vals)

@admin_required
def index(request, start=0, count=10):
    offset = start
    more_posts = False 
    posts = BlogPost.all().order('-published').fetch(count+1, offset)
    if len(posts) > count:
        posts = posts[0:count]
        more_posts = True
    template_vals = {
            'offset': offset,
            'count': count,
            'last_post': offset + len(posts) - 1,
            'prev_offset': max(0, offset - count),
            'next_offset': offset + count,
            'posts': posts,
            'more_posts': more_posts,
            'config': config,
            'menu_view': True,
            }
    return render_to_response("blog/admin/index.html", template_vals)

@admin_required    
def regenerate_site(request):
    """Regenerate entire site"""
    deferred.defer(regenerate)
    deferred.defer(post_deploy, BLOGOKAY_VERSION)
    return render_to_response('blog/admin/regenerating.html', 
                             {'config': config,})

        
