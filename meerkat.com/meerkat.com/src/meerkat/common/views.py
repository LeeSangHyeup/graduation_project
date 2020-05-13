# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import Context
from meerkat.settings import TEMPLATE_DIRS


def main_Page(request):
    context = Context({
        'user':request.user,
        'base':TEMPLATE_DIRS[0]+'/common/base.html'
                   })
    return render_to_response('common/main.html', context)