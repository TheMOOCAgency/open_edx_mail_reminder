# -*- coding: utf-8 -*-

import os

import logging
import smtplib

import json
import logging
import re

path = "/edx/app/edxapp/edx-platform/lms/djangoapps/tma_apps/mailtester/"

users_obj = {}
	
def json_record(user_mail_json):
	with open(path+'data.json', 'r+') as f:
		try :
			data = json.load(f)
			users_obj = data
			try :
				user_line = users_obj[user_mail_json]
				users_obj[user_mail_json] =  user_line+1
				f.seek(0)
				json.dump(users_obj, f, indent=4)
			except :
				users_obj[user_mail_json] = 1
				f.seek(0)
				json.dump(users_obj, f, indent=4)
		except :
			new_user = {user_mail_json:1}
			json.dump(new_user, f, indent=4)


def json_check(user_mail_json):
	with open(path+'data.json', 'r+') as f:
		try :
			data = json.load(f)
			users_obj = data
			mail_limit = 3
			user_limited = False
			try :
				user_line = users_obj[user_mail_json]
				if user_line >=3 :
					user_limited = True
			
			except :
				user_limited = False
			
		except :
			user_limited = False
	return user_limited
			
print(json_check("daivis"))







		