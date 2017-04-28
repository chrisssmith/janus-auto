import requests
import pprint
import mongodb
from pandas import DataFrame
import json
import secrets
survey_id = secrets.survey_id
mongodb.db_init()
url1 = 'https://api.smartsurvey.io/v1/surveys/%s' % survey_id
url2 = 'https://api.smartsurvey.io/v1/surveys/%s/responses' % survey_id

page_size = 50


params = {
  'api_token':secrets.api_token,
  'api_token_secret':secrets.api_token_secret,
  'include_labels': 'true',
  'page_size': page_size
}

r1 = requests.get(url1,params=params)  # High Level Survey Data




survey_details = json.loads(r1.text)
number_of_responses =  survey_details["responses"]
print "Number of responses = " + str(number_of_responses)
iterations = (number_of_responses / page_size) + 1
print "iterations needed = " + str(iterations)
survey = r1.json()
i = 0
counter = 0
page = 0
output = {}

while(counter<iterations):
    print counter
    params2 = {
      'api_token':'5xgPHR5ZTyaBXYJDkLfoOEIhaArCkBOM',
      'api_token_secret':'2JprHhwQVGTSNqn',
      'include_labels': 'true',
      'page_size': page_size,
      'page': counter
    }
    r2 = requests.get(url2,params=params2)  # Low Level Survey Responses
    responses = r2.json()




    for response in responses:

        output[i] = {}

        for page in response['pages']:

            for question in page['questions']:

                uid = question['number']
                title = question['title']

                if question['type'] == 'open_ended':
                    try:
                        answer = question['answers'][0]['value']
                    except KeyError:
                        pass

                if question['type'] == 'file_upload':
                    answer = question['answers'][0]['value']

                if question['type'] == 'single_choice':
                    answer = question['answers'][0]['choice_title']

                elif question['type'] == 'checkbox':
                    answer = question['answers'][0]['choice_title']

                elif question['type'] == 'radio':
                    answer = question['answers'][0]['choice_title']

                elif question['type'] == 'multiple_choice':
                    answer = ' '
                    for item in question['answers']:
                        answer = answer + item['choice_title'] + ' '

                output[i][uid] = answer
                #print answer
                #print output[i]
        i += 1
    counter = counter + 1




def extract_surevy_responses():

    data = {}
    for response in output:
        # print output[response]

        # pp.pprint(output[response])
        response = output[response]
        #print ""
        for question in response:
            #print str(question) + " - " + response[question]
            data[str(question)] = response[question]
        mongodb.insert_to_db(data)
        data = {}
    print str(len(output)) + " survey responses added to MongoDB"