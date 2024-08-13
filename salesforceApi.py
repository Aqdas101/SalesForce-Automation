import requests
import loggingConfig
from loggingConfig import logger
from emailSender import sent_email
from datetime import datetime




#Salesforce API request body URI
def get_salesforce_data(authKey):

  access_token = authKey
  try:
    url = '''https://parsons.my.salesforce.com/services/data/v54.0/query/?q=SELECT 
          ID, 
          CaseNumber, 
          Subject, 
          Description, 
          Status, 
          ContactID, 
          Contact.Name, 
          Contact.EmployeeNumber__c,
          Last_Working_Date __c, 
          Category__c, 
          AffectedItem__c, 
          Parent.Id, 
          Parent.CaseNumber, 
          Contact.WorkLocationCode__c, 
          Contact.GlobalBusinessUnit__c,
          Contact.Email,
          PrimaryAffectedCI__r.Name, 
          LastModifiedDate
          FROM 
            Case     
              WHERE RecordTypeID = '01241000001MC5XAAW'    
                AND QueueName__c = 'Platform Applications'    
                AND OwnerId IN ('00541000006nPbKAAU','00G2M000003KK2qUAG')    
                AND Status IN ('Completed','Closed')    
                AND Origin IN ('Self-Service','AutoTerm Service')   
                AND (               
                    Category__c = 'Applications'                     
                    AND AffectedItem__c = 'Enterprise Business Apps'                     
                    AND PrimaryAffectedCI__r.Name = 'SharePoint (Office 365)'
                  )
    '''

    payload = {}

    headers = {
        'Authorization':
        f'Bearer {access_token}',
        'Cookie':
        'BrowserId=zoAZPhodEe-brLPJ5M2-FA; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1'
    }

    # Make the GET request to the API
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    data = response.json()

    print("Successfully fetched data from Salesforce API")
    logger.info('Successfully fetched data from Salesforce API')

    return data

  except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    logger.error(f"Request failed: {e}")
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    subject = 'Error in SalesForce Automation'
    body = f'{current_time}: Failed to get access token: {e}'
    sent_email(email_body=body, email_subject=subject)
    raise SystemExit(e)
