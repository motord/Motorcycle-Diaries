# -*- coding: utf-8 -*-
"""
sms.views
"""

"""
import logging

from google.appengine.api import users
from google.appengine.api import memcache
from werkzeug import (
  unescape, redirect, Response,
)
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest
)

from kay.utils import (
  render_to_response, reverse,
  get_by_key_name_or_404, get_by_id_or_404,
  to_utc, to_local_timezone, url_for, raise_on_dev
)
from kay.i18n import gettext as _
from kay.auth.decorators import login_required

"""

import logging
from werkzeug import Response
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest, HTTPException
)
import PyFetion
from sms.forms import MessageForm

# Create your views here.

def index(request):
    form = MessageForm()
    if request.method == 'POST':
        #if form.validate(request.form):
            #message = form.save()
            #phone = PyFetion.PyFetion(message.sender, message.password, "HTTP")
            #try:
            #    phone.login()
            #    phone.send_sms(message.content, message.receiver)
            #except PyFetion.PyFetionSocketError, e:
            #    raise HTTPException()
      return Response('OK')
