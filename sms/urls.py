# -*- coding: utf-8 -*-
# sms.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('sms/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'sms/index': 'sms.views.index',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='sms.views.index'),
  )
]

