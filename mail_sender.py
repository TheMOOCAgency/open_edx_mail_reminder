# -*- coding: utf-8 -*-

import os
import settings
import logging
import smtplib

import json
import logging
import re

import sys
import datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
sys.path.append("/edx/app/edxapp/edx-platform/lms/djangoapps/tma_apps")
sys.path.append("/edx/app/edxapp/edx-platform/lms/djangoapps")


from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST,require_GET,require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth import authenticate, login


# mailing
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# mailing

from datetime import date
from dateutil.parser import parse

# Json check user limits for mailing
from json_creator import json_record, json_check


log = logging.getLogger(__name__)

user_dict_test = {'first_name': 'Agathe', 'relay': 1, 'mailInfo': [1, 2], 'userMail': 'daivis.hubbel@themoocagency.com', 'course_id': 'course-v1:nautisme-durable+2018+2019', 'nbrWorks': 2}

org ="ATEE"



@csrf_exempt
def mail_sender(user_email,template):
	toaddr = user_email
	# log.warning("__________________________________get__READY_to_rumble____")
	cc = ['daivis.hubbel@themoocagency.com']
	html = template

	part2 = MIMEText(html, 'html')
	fromaddr = 'The MOOC Agency MOOC ATEE<no-reply@themoocagency.com>'
	toaddr = 'daivis.hubbel@themoocagency.com'
	# toaddr = str(email)
			# toaddr = recipient
	toaddrs = [toaddr] + cc
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = 'Votre parcours apprenant.'
	server = smtplib.SMTP('mail3.themoocagency.com', 25)
	server.starttls()
	server.login('contact', 'waSwv6Eqer89')
	msg.attach(part2)
	text = msg.as_string()
	log.warning("message sent to___"+str(toaddr))
	server.sendmail(fromaddr, toaddrs, text)
	server.quit()

def mail_sender_template(user_dict_a) : 
	user_dict_b = user_dict_a
	log.warning(user_dict_b)
	first_name_mail = str(user_dict_b["first_name"])
	course_name_mail = str(user_dict_b["course_id"])
	nbr_work_mails = str(user_dict_b["nbrWorks"])
	relay_mail = str(user_dict_b["relay"])
	user_mail_mail = str(user_dict_b["userMail"])
	course_not_step_mail = define_name_of_work(nbr_work_mails,relay_mail)
	course_name_mail= str(user_dict_b["course_id"])
	mail_template = "<html><head></head><body><p>Bonjour "+str(first_name_mail)+",</p><p>Vous &ecirc;tes inscrit au cours &#58; <span style='font-weight:bold'>"+str(course_name_mail)+"</span></p><p>Vous ne vous &ecirc;tes pas connect&eacute; depuis 7 jours et vous n&apos;avez toujours pas fini ce cours.</p><p>En effet, il vous reste <span style='font-weight:bold'>"+str(course_not_step_mail)+"</span> &agrave; terminer.</p><p>Nous souhaitions vous informer, qu&apos;en cas de diffult&eacute;s le forum de dicussion est disponible pour &eacute;changer avec l&apos;&eacute;quipe enseignante et les autres apprenants</p><p></p><p>&Agrave; tr&eacute;s bient&ocirc;t</p><p>L&apos;&eacute;quipe&nbsp;"+str(org)+".</p></body> </html>"

	return(mail_sender(user_mail_mail,mail_template))
	# print(mail_template)


def main(arr_input):
   numbers = arr_input
   smallest = numbers[0]
   for i in range(0,len(numbers),1):
      if (numbers[i] < smallest):
         smallest = numbers[i]
   return smallest


def prepare_list_for_mailing(list) :
	h = 0
	array = list
	for i in range(len(array)):
		userDict = array [i]
		user_name = userDict["email"]
		arrayUser = []
		userDict_to_mail = {}
		dayOff = userDict["last_connexion"]   
		nbrWorks = userDict["nbrWorks"]   
		if dayOff > 7 :   
			grade_final= userDict["grade_final"].strip('%')
			grade_final_float= float(grade_final)
			arrayUser = []
			if grade_final_float < 100 :
				for h in range(nbrWorks):
					checkEvalto = userDict["eval"+str(h+1)].strip('%')
					checkEvaltoNumber = float(checkEvalto)

					if checkEvaltoNumber == 0 :
						user_name = userDict["email"]
						arrayUser.append(h+1)
			userDict_to_mail["mailInfo"] = arrayUser  
			userDict_to_mail["nbrWorks"] = nbrWorks  
		userDict_to_mail["userMail"] = user_name
		userDict_to_mail["first_name"] = userDict["first_name"]
		userDict_to_mail["course_id"] = userDict["course_id"]
			
		try :
			userDict_to_mail["relay"] = main(arrayUser)
			try : 
				json_check(user_name)
				if json_check(user_name) == False: 
					mail_sender_template(userDict_to_mail)
					json_record(user_name)
			except :
				json_record(user_name)
				mail_sender_template(userDict_to_mail)

		except:	
			userDict_to_mail["relay"] = "no value"	
		



def define_name_of_work(nbr_works,relay) :
	string_to_mail = ""
	works_total = nbr_works
	relay = relay
	str_for_weeks = "LA&nbsp;SEMAINE&nbsp;"
	str_for_final_test = "L&apos;&Eacute;VALUTION FINAL"
	if relay < nbr_works :
	    string_to_mail = str_for_weeks+str(relay)
	elif relay == nbr_works :
		string_to_mail = str_for_final_test
	   
	return string_to_mail	   
	   
   
def prepare_and_send(list) : 
	prepare_list_for_mailing(list)

