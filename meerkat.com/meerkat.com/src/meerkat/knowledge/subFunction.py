# -*- coding: utf-8 -*-
from django.template import RequestContext
from meerkat.settings import TEMPLATE_DIRS

def makeExceptionMsgContext(request, msg):
    context = RequestContext(request, {
        'base':TEMPLATE_DIRS[0]+'/common/base.html',
        'msg':msg
        })
    return context