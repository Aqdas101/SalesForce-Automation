import requests
import json
import loggingConfig
from loggingConfig import logger

def get_queue_id(queue_name: str = 'Cloud Productiviy Solution') -> str:
  """Get Queue Name, and return queue ID"""
  try:
    instance_url = ''
    api_version = ''
    access_token = ''

    headers = { 'Authorization': f'Bearer {access_token}',
              'Content-Type': 'application/json'}

    query_url = f"{instance_url}/services/data/{api_version}/query/?q=SELECT+Id+FROM+Group+WHERE+Type=\'Queue\'+AND+Name=\'{queue_name}\""

    response = requests.get(query_url, headers=headers)
    # queue_id = response.json()['records'][0]['Id']

    logger.info(f"Successfully fetched queue ID's for queue name {queue_name}")
    return response.json()

  except Exception as e:
    logger.error(f"Failed to get queue Id for {queue_name}: {e}")
    return None


def assign_case_to_queue(case_id: str, queue_id: str) -> str:
    """Assign Case to Queue"""

    instance_url = ''
    api_version = ''
    access_token = ''

    headers = { 'Authorization': f'Bearer {access_token}',
              'Content-Type': 'application/json'}

    update_url = f'{instance_url}/services/data/{api_version}/sobjects/Case/{case_id}'
    data = {'OwnerId': queue_id}

    response = requests.patch(update_url, headers=headers, json=data)

    if response.status_code == 204:

      logger.info('Case assigned to queue successfully')
      return 'Case assigned to queue successfully'

    else:
      logger.error('Failed to assign case to queue:', response.json())
      return 'Failed to assign case to queue:', response.json()


def case_closure(case: dict, Token: dict, exception: dict, uri_env: str):
  """Case Closure Code"""
  try:
    access_token = Token['access_token']
    message = exception['Message']
    description = case['Description']
    subject = case['Subject']
    case_id = case['Id']
    uri_env = ''
    case_number = case['caseNumber']


    headers = {
        "content-type": "application/json;odata=verbose",
        "Authorization": f"OAuth {access_token}",
        "SForce-Auto-Assign": "FALSE"
    }

    body = {
        # "Status": "Completed",
        # "ClosureCode__c": "Resolved by OO Automation",
        # "SolutionDetails__c": f"Site Created {siteurl}",
        "Subject": f"{subject} - Need Manual Setup",
        "Description": f"{description}\n Error \n {message}",
        "RunAssignmentRules__c": 0
    }

    body_json = json.dumps(body)
    uri = f"{uri_env}/services/data/v54.0/sobjects/case/{case_id}"

    # Test URI
    # uri = f"{url_env}/services/data/v54.0/sobjects/case/5003h00000OVPwHAAX"

    response = requests.patch(uri, headers=headers, data=body_json)
    # print(f"AF488: Case {case_id} {case_number} Successful Site Created")
    logger.info(f"AF488: Case {case_id} {case_number} Successful Site Created")
    return "AF488: Case {case_id} {case_number} Successful Site Created"

  except Exception as e:
    logger.error(f"Failed to run case closure script: error{e}")
