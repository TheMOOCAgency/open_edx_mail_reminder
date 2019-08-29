# -*- coding: utf-8 -*-

import os

import logging
import smtplib

import json
import logging
import re

path = "/edx/app/edxapp/edx-platform/lms/djangoapps/tma_apps/mailtester/"

users_obj = {}
	
def tma_graded_scorable_blocks_to_header(user_mail_json):
	with open(path+'data.json', 'r+') as f:
		try :
			data = json.load(f)
			users_obj = data
			try :
				user_line = users_obj[user_mail_json]
				users_obj[user_mail_json] =  user_line+1
				f.seek(0) 
			except :
				users_obj[user_mail_json] = 1
				json.dump(users_obj, f, indent=4)
		except :
			new_user = {user_mail_json:1}
			json.dump(new_user, f, indent=4)

tma_graded_scorable_blocks_to_header("daivis")