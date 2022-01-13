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
        data = requests.get("https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true").json()
         
        entities = tracker.latest_message['entities']
         
        states = None
         
        for e in entities:
            if e['entity'] == "state":
                states = e['value']
                     
            for i in data["regionData"]:
                
                if i["region"] == states.title():
                    
                    # covid stats message
                    cases = ('Active Cases :' + str(i['activeCases']) +
                                 '\nNew Infected Cases :' +str(i['newInfected'])+
                                ' \nTotal Infected : '+str(i['totalInfected']) +
                                ' \nRecovered : ' +str(i['recovered']) +
                                '\nDeceased :' +str(i['deceased']) + '\nNewly Recovered :'+
                                str(i['newRecovered']))
                    
        dispatcher.utter_message(text = cases )

        return []
