from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.domain import Domain
import rasa_core.trackers 

import logging
logger = logging.getLogger(__name__)

import requests
import json

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.events import UserUtteranceReverted
from rasa_core_sdk.events import AllSlotsReset
from rasa_core_sdk.events import Restarted

class SaveOrigin(Action):
	def name(self):
		return 'action_save_origin'
		
	def run(self, dispatcher, tracker, domain):
		orig = next(tracker.get_latest_entity_values("location"), None)
		if orig == 'Bangalore':
			orig = 'BLR'
		elif orig == 'Delhi':
			orig = 'DEL'
		elif orig == 'Mumbai':
			orig = 'BOM'
		elif orig == 'Hyderabad':
			orig='HYD'
		elif orig == 'Chennai':
			orig = 'MAA'
		elif orig == 'Kolkata':
			orig = 'CCU'	
		if not orig:
			dispatcher.utter_message("Please enter a valid airport code")
			return [UserUtteranceReverted()]
		return [SlotSet('from',orig)]
	


class SaveDestination(Action):
	def name(self):
		return 'action_save_destination'
		
	def run(self, dispatcher, tracker, domain):
		dest = next(tracker.get_latest_entity_values("location"), None)
		if dest == 'Bangalore':
			dest = 'BLR'
		elif dest == 'Delhi':
			dest = 'DEL'
		elif dest == 'Mumbai':
			dest = 'BOM'
		elif dest == 'Hyderabad':
			dest='HYD'
		elif dest == 'Chennai':
			dest = 'MAA'
		elif dest == 'Kolkata':
			dest = 'CCU'
		if not dest:
			dispatcher.utter_message("Please enter a valid airport code")
			return [UserUtteranceReverted()]
		return [SlotSet('to',dest)]
		
		
class SaveDate(Action):
	def name(self):
		return 'action_save_date'
		
	def run(self, dispatcher, tracker, domain):
		inp = next(tracker.get_latest_entity_values("date"), None)
		if inp == 'today':
			inp = '21-06-2019'
		if not inp:
			dispatcher.utter_message("Please enter a valid date")
			return [UserUtteranceReverted()]
		return [SlotSet('date',inp)]
		
class ActionSlotReset(Action): 	
    def name(self): 		
        return 'action_slot_reset' 	
    def run(self, dispatcher, tracker, domain): 		
        return[AllSlotsReset()]
		

		
from bs4 import BeautifulSoup
import urllib.request
import re


class getFlightStatus(Action):
	def name(self):
		return 'action_get_flight'
	def run(self, dispatcher, tracker, domain):
		orig=tracker.get_slot('from')
		dest=tracker.get_slot('to')
		dat=tracker.get_slot('date')
		quote_page = "https://flights.makemytrip.com/makemytrip/search/O/O/E/1/0/0/S/V0/{}_{}_{}?contains=false&remove="
		page=urllib.request.urlopen(quote_page.format(orig,dest,dat))
		soup = BeautifulSoup(page, 'html.parser')
		list1=[]
		message=soup.find_all('label',attrs={'class':'flL mtop5 mleft3 vallabel'})
		dispatcher.utter_message("Here is the list of carriers with their fare")
		for a in message:
			list1.append(a.text)	
		message1=soup.find_all('span',attrs={'class':'flR'})
		list2=[]
		for b in message1:
			if "Rs." in b.text:
				list2.append(re.sub('\s+', '', b.text))
		for i in range(len(list1)):
			dispatcher.utter_message(list1[i]+" : "+list2[i])
			print("---"+list1[i]+" : "+list2[i])
		return []

class getComInfo(Action):
	def name(self):
		return 'action_get_company_info'
	
	def run(self, dispatcher, tracker, domain):
		url_page ="https://www.easystepin.com/"
		page = urllib.request.urlopen(url_page)
		soup = BeautifulSoup(page, 'html.parser')
		message = soup.find('div', attrs={'class': 'easy_step_left'})
		results = message.find_all('p')
		print('Number of results', len(results))
		mess = []
		for p in results:
			mess.append(p.text)
		print(str(mess))
		mess1 = ''.join(mess[0:len(results)-3])

		dispatcher.utter_message(mess1)
		return[]