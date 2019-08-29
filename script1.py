#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import settings
import logging
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
sys.path.append("/edx/app/edxapp/edx-platform/lms/djangoapps/tma_apps")
sys.path.append("/edx/app/edxapp/edx-platform/lms/djangoapps")
MODULE_NAME = "tma_methods"


import logging
from django.contrib.auth.models import User
from instructor_task.tasks_helper.grades import users_for_course_v2


