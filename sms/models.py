# -*- coding: utf-8 -*-
# sms.models

from google.appengine.ext import db

# Create your models here.
class Message(db.Model):
    sender=db.StringProperty(required=True)
    password=db.StringProperty(required=True)
    reciever=db.StringProperty(required=True)
    url=db.LinkProperty(required=False)
    content=db.StringProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)