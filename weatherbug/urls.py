# -*- coding: utf-8 -*-
# weatherbug.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('weatherbug/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'weatherbug/index': 'weatherbug.views.index',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='weatherbug.views.index'),
  )
]

