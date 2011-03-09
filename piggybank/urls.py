# -*- coding: utf-8 -*-
# piggybank.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('piggybank/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'piggybank/index': 'piggybank.views.index',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='piggybank.views.index'),
  )
]

