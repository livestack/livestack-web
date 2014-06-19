#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Longgeek <longgeek@gmail.com>

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.views.generic.base import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
import models, re, threading

class Index(View):
    def get(self, request):
        context = {}
        return render_to_response('index.html', context)


class Download(View):
    def post(self, request):
        context = {}
        email = request.POST.get('email')
        who = email
        username = email[0].split('@')[0]
        password = ''
        recontact = re.compile(r'^[a-zA-Z0-9_.]{3,18}\@[a-zA-z0-9]{2,10}\.[a-zA-Z0-9]{3,10}(\.[a-zA-Z0-9]{2,10})?$')

        if recontact.match(email):
            sendmail('[LiveStack] Download LiveStack iso', [email,])
            sendmail('[LiveStack] Request download livestack iso', ['livestackgroup@thstack.com',], who)
            User.objects.create_user(username, password, email)
            User.save()
            return HttpResponse("Checkout your email right now!", context)
        else:
            return HttpResponse("ERROR: Email address is valid!", context)


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, email):
        self.subject = subject
        self.html_content = html_content
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(self.subject,
                                     self.html_content,
                                     'LiveStack',
                                     self.email)
        msg.attach_alternative(self.html_content, "text/html")
        msg.send()


def sendmail(subject, email, who=None):
    template_path = "email.html"
    for name in email:
        context = {
            'email': name.split('@')[0]
        }

        if name.split('@')[0] == 'livestackgroup':
            context = {
                'email': name.split('@')[0],
                'emailuser': who
            }

    html_content = loader.render_to_string(template_path, context)
    emails = EmailThread(subject, html_content, email)
    emails.start()
