# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
import requests
from rasa_sdk.events import SlotSet,UserUtteranceReverted


class ActionCoronaTracker(Action):

     def name(self) -> Text:
         return "action_corona_cases"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
             data = requests.get("https://api.covid19india.org/data.json").json()
         
             entities = tracker.latest_message['entities']
         
             state = None
         
             for i in entities:
                 if i['entity'] == 'state':
                     state = i['value']
             cases = "Please check and enter correct detail"
             
             if state == "India":
                 state = 'Total'
                 
             for i in data['statewise']:
                 if i['state'] == state.title():
                     
                     cases = ('Active Cases: '+i['active'] +  
                             ' Confirmed cases: '+i['confirmed'] +
                             ' Recovered: ' +i['recovered'])
             
             dispatcher.utter_message(text=cases)

             return []
