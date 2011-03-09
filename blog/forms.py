# -*- coding: utf-8 -*-
"""
Forms for creating and editing Blog Posts

:Copyright: (c) 2009 Victor Goh <victorgoh@gmail.com>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.utils.forms.modelform import ModelForm
from kay.utils import forms

from blog.models import BlogPost

class PostForm(ModelForm):
    title = forms.TextField('Title', min_length=3, max_length=255, required=True)
    body = forms.TextField('Body', min_length=3, required=True, widget=forms.Textarea)
    tags = forms.TextField('Tags', required=True, widget=forms.Textarea)
    draft = forms.BooleanField('Draft?', required=False)
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'tags']

        