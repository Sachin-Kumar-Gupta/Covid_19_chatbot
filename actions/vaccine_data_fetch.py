
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
            df = read_pdf(pdf, area = [208, 68,800, 560], multiple_tables=False, pages = "all")[0]
            df1 = df.copy()
            df1.columns = ['State/UT','1st Dose','2nd Dose','Below 18','Precaution Dose','Total Doses']
            return df1
        
        def total(pdf):
            df2 = read_pdf(pdf, area = [114, 161,180, 538], multiple_tables=False, pages = "all")[0]
            df3 = df2.copy()
            df3.columns = ['1st Dose','2nd Dose','Below 18','Precaution Dose','Total Doses']
            df3 = df3.replace({r'\r': ' '}, regex=True)
            return df3

        data = vaccine(pdf)
        total = total(pdf)
             
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
        '''else:
            dff = ('Overall first doses : '+total['1st Dose'][0]+total['1st Dose'][1]+
                   '\nOverall second doses : '+total['2nd Dose'][0]+total['2nd Dose'][1]+
                   '\nOverall below 18 doses : '+total['Below 18'][0]+total['Below 18'][1]+
                   '\nOverall precaution doses : '+total['Precaution Dose'][0]+total['Precaution Dose'][1]+
                   '\nOverall vaccinations : '+total['Total Doses'][0]+total['Total Doses'][1])
                    '''
        dispatcher.utter_message(text = dff)

        return []

        
