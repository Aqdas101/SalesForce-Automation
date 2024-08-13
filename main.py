from tokenApi import get_access_token
from salesforceApi import get_salesforce_data
from dataFormation import process_salesforce_data, save_results_to_file
from queue_assignment import get_queue_id, assign_case_to_queue, case_closure

import loggingConfig
from loggingConfig import logger

import json
import os
import requests
# from dotenv import load_dotenv



# load_dotenv()

# client_id = os.getenv('CLIENT_ID')
# client_secret = os.getenv('CLIENT_SECRET')
# username = os.getenv('USERNAME')
# password = os.getenv('PASSWORD')

# auth_key = get_access_token(client_id, client_secret, username, password) # Salesforce API Acess Token
# auth_key = os.environ['AUTH_KEY']


# data = get_salesforce_data(auth_key)

#------test-------
with open('/content/response.json', 'r') as file:
  data = file.read()
data = json.loads(data)
#-------test-------


processed_data = process_salesforce_data(data)
filename = "processed_salesforce_data.json"
save_results_to_file(processed_data, filename)

for i in range(len(processed_data)):
  try:
    NPIM = processed_data[i]['data']['descriptionFields'][ 'Needs Project Information Management']

    if NPIM.capitalize() == 'No':
      logger.info('Running assign queue funciton')
      # queue_id = get_queue_id()
      # assign_case_to_queue(queue_id)
      logger.info('Case assigned To queue successfully')
    else:
      print('Running Case Closure Code')
      # case_closure()
  except Exception as e:
    logger.error(f"Error at: {processed_data[i]['data']['caseID']}")
    continue
