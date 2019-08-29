# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.conf import settings
import json
import logging
import re
import os
import sys
import datetime
from datetime import date
from dateutil.parser import parse
from colorama import Fore, Back, Style 


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
sys.path.append("/edx/app/edxapp/edx-platform/lms/djangoapps/tma_apps")
sys.path.append("/edx/app/edxapp/edx-platform/lms/djangoapps")

from django.utils.translation import ugettext as _

from tma_task.tasks import task_generate_users_from_csv
from courseware.courses import get_course_by_id, get_courses

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.views.decorators.http import require_POST,require_GET,require_http_methods
from django.views.decorators.csrf import csrf_exempt

from collections import OrderedDict, defaultdict

from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from tma_ensure_form.utils import ensure_form_factory

from courseware.courses import get_course_by_id
from openedx.core.djangoapps.course_groups.models import CohortMembership, CourseUserGroup
from openedx.core.djangoapps.course_groups.cohorts import get_cohort, is_course_cohorted

from lms.djangoapps.grades.new.course_grade import CourseGradeFactory
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from opaque_keys.edx.keys import CourseKey, UsageKey
from opaque_keys import InvalidKeyError

from lms.djangoapps.tma_grade_tracking.models import dashboardStats

from student.models import User, UserProfile,CourseEnrollment
from edxmako.shortcuts import render_to_response
from util.json_request import JsonResponse, expect_json

from lms.djangoapps.grades.context import grading_context_for_course

from tma_apps.tma_support_functions import is_course_opened, is_enrollment_opened
from tma_task.api_helper import submit_task

from microsite_configuration.models import Microsite
from mail_sender import prepare_and_send

log = logging.getLogger(__name__)


# def testMail(self):
        # _microsite = configuration_helpers.get_value('domain_prefix')
        # return JsonResponse(_microsite)
        
responseInDict = {}

tree = lambda: defaultdict(tree)

valueArr = []
bigNar = []
dictoBlee = tree()



def tma_graded_scorable_blocks_to_header(course_key):
	"""
	Returns an OrderedDict that maps a scorable block's id to its
	headers in the final report.
	"""
	scorable_blocks_map = OrderedDict()
	grading_context = grading_context_for_course(course_key)
	for assignment_type_name, subsection_infos in grading_context['all_graded_subsections_by_type'].iteritems():
		for subsection_index, subsection_info in enumerate(subsection_infos, start=1):
			for scorable_block in subsection_info['scored_descendants']:
				header_name = (
					u"{assignment_type} {subsection_index}: "
					u"{subsection_name} - {scorable_block_name}"
				).format(
					scorable_block_name=scorable_block.display_name,
					assignment_type=assignment_type_name,
					subsection_index=subsection_index,
					subsection_name=subsection_info['subsection_block'].display_name,
				)
				scorable_blocks_map[scorable_block.location] = header_name
	return scorable_blocks_map


def testMail(self):

	course_key_string = "course-v1:nautisme-durable+2018+2019"
	course_key = CourseKey.from_string(course_key_string)
	requestFalse = {"fields":["user_id","email","first_name","last_name","situation_professionnelle","inscription_date","last_connexion","time_tracking","grade_detailed","exercises_grade","grade_final","certified","cohorte_names","cp","phone_number"],"receivers":["daivis.hubbel@themoocagency.com"]}

	otoMicrosite = configuration_helpers.get_value('domain_prefix')


	report_fields = requestFalse.get('fields')
	register_fields = configuration_helpers.get_value('FORM_EXTRA')
	certificate_fields = configuration_helpers.get_value('CERTIFICATE_FORM_EXTRA')

	course=get_course_by_id(course_key)
	microsite_information = Microsite.objects.get(key=otoMicrosite)

	form_factory = ensure_form_factory()
	form_factory.connect(db='ensure_form',collection='certificate_form')

	#Dict of labels
	form_labels={
		"last_connexion":_("Last login"),
		"inscription_date":_("Register date"),
		"user_id":_("User id"),
		"email":_("Email"),
		"grade_final":_("Final Grade"),
		"cohorte_names":_("Cohorte name"),
		"time_tracking":_("Time spent"),
		"certified":_("Attestation"),
		"username":_("Username"),
	}
	for field in register_fields :
		form_labels[field.get('name')]=field.get('label')
	for field in certificate_fields :
		form_labels[field.get('name')]=field.get('label')

	#Identify multiple cells fields
	multiple_cell_fields=["exercises_grade","grade_detailed"]

	#Is report cohort specific?
	course_cohorted=is_course_cohorted(course_key)
	cohortes_targeted = []
    
	course_enrollments=CourseEnrollment.objects.filter(course_id=course_key, is_active=1)
	grade_summary={}
	user_certificate_info = {}
	
	for enrollment in course_enrollments :
            if not enrollment.is_active:
                continue
            #Gather user information
            user= enrollment.user
            user_grade = CourseGradeFactory().create(user, course)
            graded_scorable_blocks = tma_graded_scorable_blocks_to_header(course_key)

            for section_grade in user_grade.grade_value['section_breakdown']:
                grade_summary[section_grade['category']]=section_grade['percent']
            try:
                custom_field = json.loads(UserProfile.objects.get(user=user).custom_field)
            except:
                custom_field = {}

            user_certificate_info = {}
            try:
                form_factory.microsite = self.microsite
                form_factory.user_id = user.id
                user_certificate_info = form_factory.getForm(user_id=True,microsite=True).get('form')
            except:
                pass

            valueArrB = []
            dictSelection = {}
            userDict = {}
            for field in report_fields :
                userDict["course_id"] = str(course_key)
                if field in multiple_cell_fields:
                   
                    if field=="grade_detailed":
                        i = 0
                        for section in grade_summary :
                            print("len(section)") 
                            print(len(section))
                            i += 1
                            eval = "eval"
                            evalstr = eval + str(i)
                            section_grade = str(int(round(grade_summary[section] * 100)))+'%'
                            userDict[evalstr] = section_grade
                            userDict["nbrWorks"] = i
                else :
                    value=''
                    if field=="user_id":
                        value=user.id
                        userDict[field] = value
                    elif field=="email":
                        value=user.email
                        userDict[field] = value
                    elif field=="first_name":
                        try :
                            if user.first_name:
                                value=user.first_name
                                userDict[field] = value
                            elif custom_field :
                                value=custom_field.get('first_name', 'unkowna')
                                userDict[field] = value
                            else :
                                value='unknown'
                                userDict[field] = value
                        except :
                            value='unknown'
                            userDict[field] = value
                    elif field=="last_name":
                        try :
                            if user.last_name:
                                value=user.last_name
                                userDict[field] = value
                            elif custom_field:
                                value=custom_field.get('last_name', 'unkowna')
                                userDict[field] = value
                        except :
                            value='unknown'
                            userDict[field] = value
                    elif field=="last_connexion":
                        try :
                            dateR=user.last_login.strftime('%m-%d-%y')
                            dt = parse(str(dateR))
                            f_date = dt.date()
                            l_date = str(datetime.date.today())
                            g_date = parse(l_date)
                            h_date = g_date.date()
                            delta = h_date - f_date
                            if not delta :
                                deltaStr = 0
                            elif delta == "":
                                deltaStr = 0
                            else :
                                deltaStr = str(delta.days)
                            userDict[field] = deltaStr
                            
                        except:
                            value=''
                            userDict[field] = value
                    elif field=="inscription_date":
                        try :
                            value=user.date_joined.strftime('%d-%m-%y')
                            userDict[field] = value
                        except:
                            value=''
                            userDict[field] = value
                    elif field=="certified":
                        if user_grade.passed :
                            value = _("Yes")
                            userDict[field] = value
                        else :
                            value = _("No")
                            userDict[field] = value
                    elif field=="grade_final":
                        value = str(int(round(user_grade.percent * 100)))+'%'
                        userDict[field] = value
                    elif field=="username":
                        value=user.username
                        userDict[field] = value
                      
            cut = len(course_enrollments)        
            bigNar.append(userDict) 
            res = bigNar[0 : cut] 
	prepare_and_send(bigNar)        
	return JsonResponse(res)
			 
