# -*- coding: utf-8 -*-

from kay.utils.forms.modelform import ModelForm
from kay.utils import forms

from sms.models import Message

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['sender', 'password', 'reciever', 'url', 'content']

        