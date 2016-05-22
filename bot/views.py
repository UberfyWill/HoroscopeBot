# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json, requests, wikipedia, re, wolframalpha
from .models import Horoscope, UserData, Subscribe
from datetime import datetime as dt
import spell_check
from django.conf import settings

def home(request):
	strr = """There are twelve signs in the Zodiac, one for 
	each month of the year. Unfortunately, the signs and the 
	calendar don’t align perfectly. The Zodiac begins in mid-March,
	 not on January 1st and signs span from roughly the 20th or 21st
	  of one month to the 19th or 20th of the next, not the 1st to 
	  the 31st. When someone asks you what your sign is, they’re 
	referring to your Sun Sign — where the Sun was in the Zodiac at the 
	exact moment of your birth. But every other planet in your birth
	chart is also located in a particular sign, and is influenced 
	by that sign’s unique energy. This explains why everyone who’s
	born under the influence of the same Sun Sign can still have 
	such vastly different personalities: each of us is made up of a 
	complex and unique combination of influences from the twelve signs,
	the twelve houses and all the planets, asteroids and points. And 
	having lots of planets in a certain sign in your chart will 
	only intensify that sign’s influence in your life."""
	return HttpResponse(str(strr))

def wol(query):
  client = wolframalpha.Client('9L89KG-Y23X6THEA8')
  res = client.query(query)
  return res

def wiki(query):
	try:
		array = wikipedia.search(query)
		if len(array) > 0:
			var = wikipedia.summary(array[0], sentences = 1)
			var = var.encode('ascii','ignore')
			k = re.sub(r'\([^)]*\)', '',var)
			word1 = " ".join(re.findall("[a-zA-Z]+", k))
			return str(word1)
		else:
			return str('Sorry, we could not find any match.')
	except:
		return str('Sorry, we could not find any match.')


def get_horoscope(sign):
	todays_date = dt.strftime(dt.now(), "%d-%m-%Y")
	obj = Horoscope.objects.filter(horoscope_date=todays_date, sign__icontains=sign)[0]
	print obj,"objobj"
	res = {'sign':obj.sign, 'overview': obj.overview, 'horoscope': obj.horoscope, 'horoscope_date': obj.horoscope_date}
	return res

def save_user_data(user_id, mid, msg_txt, timestamp, page_id, recent_question):
	u = UserData(user_id=user_id, mid=mid, msg_txt=msg_txt, timestamp=timestamp, page_id=page_id, recent_question= recent_question)
	u.save()
	print "User Data saved"

def send_message(user_id, query=None):
	if query!=None:
		result = get_horoscope(query)
	else:
		result = {}
	print result
	text_to_send = result.get('horoscope', 'Sorry, horoscope not available')
	text_list = []
	first_part = text_to_send[0:320].rfind('.')
	text_list.append(text_to_send[0:first_part+1])
	text_list.append(text_to_send[first_part+1:-1])
	text_list.insert(0, "Today's Horoscope")

	for each_msg_part in text_list:
		data = {
		   	"recipient":{
		        "id": user_id
		    }, 
		    "message":{
		        "text": each_msg_part
		    }
			}
		print data,"datadata"
		r = requests.post(settings.FB_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})

def send_subscribe_button(user_id):
	data = {
		   	"recipient":{
		        "id": user_id
		    }, 
		    "message":	{
		    "attachment":{
		    "type":"template",
		    "payload":	{
			        "template_type":"button",
			        "text":"Subscribe for daily horoscope every morning ?",
			        "buttons":[
						          {
						            "type":"postback",
						            "title":"Yes",
						            "payload":"Subscribe"
						          },
						          {
						            "type":"postback",
						            "title":"No",
						            "payload":"Unsubscribe"
						          }
			        			]
			      		}
		    }
		  }
		}
	r = requests.post(settings.FB_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})

def send_this(text, user_id):
	data = {
		   	"recipient":{
		        "id": user_id
		    }, 
		    "message":{
		        "text": text
		    }
			}
	print "in send_this-----------"
	r = requests.post(settings.FB_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})
	print r.text

def get_user_recent_question(user_id):
	obj = UserData.objects.filter(user_id=user_id).order_by('-timestamp')[0]
	return obj.recent_question

def get_user_recent_message(user_id):
	obj = UserData.objects.filter(user_id=user_id).order_by('-timestamp')[0]
	return obj.msg_txt


def is_subscribed(user_id):
	res = Subscribe.objects.filter(user_id=user_id)
	if len(res) == 0:
		return False
	else:
		return res[0].subscribed


def subscribe_user(user_id):
	print "in subscribe_user"
	res = Subscribe.objects.filter(user_id=user_id)
	print res, "resresres"
	if len(res) == 0:
		print "in if"
		s = Subscribe(user_id=user_id, frequency='daily', subscribed=True)
		s.save()
	else:
		res[0].subscribed = True
		res[0].save()

def unsubscribe_user(user_id):
	res = Subscribe.objects.filter(user_id=user_id, subscribed=True)
	if len(res) == 0:
		send_this("You are not subscribed.\n Thank You.", user_id)
		return False
	else:
		print "in else unsub"
		res[0].subscribed = False
		res[0].save()
		return True


def webhook(request):
	if request.method=="GET":
		token = request.GET.get('hub.verify_token',-1)
		hubchallenge = request.GET.get('hub.challenge',-1)
		if token=="9590283524":
			return HttpResponse(str(hubchallenge))
		return "GET Request made with no params"

	print request.body
	object_json = json.loads(request.body)
	res = {}
	if 'entry' in object_json and 'postback' in object_json['entry'][0]['messaging'][0]:
		payload = object_json['entry'][0]['messaging'][0]['postback']['payload']
		page_id = object_json['entry'][0]['messaging'][0]['recipient']['id']
		user_id = object_json['entry'][0]['messaging'][0]['sender']['id']
		timestamp = object_json['entry'][0]['messaging'][0]['timestamp']
		print payload, user_id
		if payload == "Capricorn":
			mid = 0
			starting_ques = "What is your horoscope Sign ?"
			msg_txt = "Start Chatting"
			send_this(starting_ques, user_id)
			save_user_data(user_id, mid, msg_txt, timestamp, page_id, starting_ques)		
			return HttpResponse("ok")

		if payload == "Subscribe":
			print "start subscribe"
			subscribe_user(user_id)
			print "after subscribe method"
			send_this("You are subscribed. Thank You.", user_id)
			send_this("I wouldn't like but if you want to unsubscribe then just message me 'Unsubscribe'.", user_id)
			return HttpResponse("ok")
		if payload == "Unsubscribe":
			send_this("No problem. Thank You", user_id)
			return HttpResponse("ok")



	elif 'entry' in object_json and 'delivery' not in object_json['entry'][0]['messaging'][0]:
		mid = object_json['entry'][0]['messaging'][0]['message']['mid']
		msg_txt = object_json['entry'][0]['messaging'][0]['message']['text']
		page_id = object_json['entry'][0]['messaging'][0]['recipient']['id']
		user_id = object_json['entry'][0]['messaging'][0]['sender']['id']
		timestamp = object_json['entry'][0]['messaging'][0]['timestamp']
		res = {'mid':mid, 'msg_txt': msg_txt, 'page_id': page_id, 'user_id': user_id, 'timestamp': timestamp}
		print res
		recent_question = get_user_recent_question(user_id)

		if 'unsubscribe' in msg_txt.lower():
			rep = unsubscribe_user(user_id)
			if rep==True:
				send_this("You are unsubscribed. Thank You.", user_id)
			return HttpResponse("ok")			
		if msg_txt.lower().split(' ')[0] in settings.YES and "Did you mean" in recent_question:
			query_sign = recent_question.split(' ')[3]
			send_message(user_id, query=query_sign)
			save_user_data(user_id, mid, msg_txt, timestamp, page_id, "horoscope")
			if not is_subscribed(user_id):
				send_subscribe_button(user_id)
			return HttpResponse("ok")
		if msg_txt.lower() in settings.SIGN_LIST:
			send_message(user_id, query=msg_txt)
			save_user_data(user_id, mid, msg_txt, timestamp, page_id, "horoscope")
			if not is_subscribed(user_id):
				send_subscribe_button(user_id)
			return HttpResponse("ok")
		else:
			corrected = spell_check.correct(msg_txt.lower())
			if corrected in settings.SIGN_LIST:
				q = "Did you mean "+ corrected.title() + " ?"
				send_this(q, user_id)
				save_user_data(user_id, mid, msg_txt, timestamp, page_id, q)
				return HttpResponse("ok")
			general_ques = "Can you please tell me your Horoscope Sign ?"
			if recent_question==general_ques:
				general_ques = "Sorry I am just a HoroscopeBot now, I trying to learn hard."
				send_this(general_ques, user_id)
				save_user_data(user_id, mid, msg_txt, timestamp, page_id, general_ques)

				return HttpResponse("ok")
			send_this(general_ques, user_id)
			save_user_data(user_id, mid, msg_txt, timestamp, page_id, general_ques)

	return HttpResponse("ok")

	# if 'object' in object_json:
	# 	return JsonResponse(res)
	# else:
	# 	return HttpResponse("No object found")





