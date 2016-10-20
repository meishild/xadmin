# -*- coding:utf8 -*-

# author          :haiyang.song
# email           :meishild@gmail.com
# datetime        :2016/10/20
# version         :1.0
# python_version  :2.7.7
# description     :
# ==============================================================================
import json

from django.contrib.auth.models import User
from django.http import HttpResponse


def user(request):
    user_list = User.objects.all()
    res_list = [{"id": user.id, "username": user.username, "is_staff": user.is_staff} for user in user_list]

    return HttpResponse(json.dumps(res_list, ensure_ascii=False))
