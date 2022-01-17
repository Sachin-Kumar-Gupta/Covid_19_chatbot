
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,UserUtteranceReverted

from tabula.io import read_pdf
from datetime import date, timedelta
import warnings
warnings.filterwarnings("ignore")

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class ActionVaccineTracker(Action):
    def name(self) -> Text:
         return "action_vaccine_done"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dat = date.today()
        yesterday = dat - timedelta(days = 1)
        d1 = yesterday.strftime("%d%B%Y")
         
        pdf = 'https://www.mohfw.gov.in/pdf/CummulativeCovidVaccinationReport'+d1+'.pdf'
         
        def vaccine(pdf):
            df = read_pdf(pdf, area = [208, 51.48,800, 560], multiple_tables=False, pages = "all")[0]
            df1 = df.copy()
            df1 = df1.drop(['Unnamed: 0'], axis = 1)
            df1 = df1.reset_index()
            df1 = df1.drop(['index'], axis = 1)
            df1.columns = ['State/UT','1st Dose','2nd Dose','Below 18','Precaution Dose','Total Doses']
            return df1

        data = vaccine(pdf)
             
        entities = tracker.latest_message['entities']
        #print("Entities is : {}".format(entities))
        states = ""
         
        for e in entities:
            if e['entity'] == "dose":
                states = e['value']
                     
        for i in data["State/UT"]:
            if  i == states.title():
                
                # doses stats message
                doses = data[data['State/UT']==i]
                num = doses.values.tolist()
                 
                dff = ('State Name : ' + num[0][0] +
                       '\nTotal First Doses : ' +num[0][1]+
                       '\nTotal Second Doses : '+num[0][2] +
                       '\nFirst Doses (15-18 year) : ' +num[0][3] +
                       '\nPrecaution Doses : ' +num[0][4] + 
                       '\nOverall Total Vaccination done : '+ num[0][5])
                    
        dispatcher.utter_message(text = dff)

        return []

        
