import json
import re
import loggingConfig
from loggingConfig import logger
from datetime import datetime
from emailSender import sent_email



def extract_case_data(record):
    try:
        caseSubject = record.get('Subject', '')
        caseContactWorkLocationCode = record.get('Contact', {}).get(
            'WorkLocationCode__c', '')
        caseStatus = record.get('Status', '')
        changeType = record.get('Change_Type__c', '')
        caseContactEmail = record.get('Contact', {}).get('Email', '')
        caseContactGlobalBusinessUnit = record.get('Contact', {}).get(
            'GlobalBusinessUnit__c', '')
        caseContactLastWorkDate = record.get('Last_Working_Date__c', '')
        caseSubcategory = record.get('Sub_Category__c', '')
        caseNumber = record.get('CaseNumber', '')
        caseID = record.get('Id', '')
        caseContactName = record.get('Contact', {}).get('Name', '')
        caseContactEmpId = record.get('Contact',
                                      {}).get('EmployeeNumber__c', '')
        caseDescription = record.get('Description', '')
        caseCategory = record.get('Category__c', '')
        adGroupList = record.get('Ad_Group_List__c', '')
        PrimaryAffectedCIName = record.get('PrimaryAffectedCI__r',
                                           {}).get('Name', '')

        description_fields = extract_description_fields(caseDescription)

        data = {
            'caseSubject': caseSubject,
            'caseContactWorkLocationCode': caseContactWorkLocationCode,
            'caseStatus': caseStatus,
            'changeType': changeType,
            'caseContactEmail': caseContactEmail,
            'caseContactGlobalBusinessUnit': caseContactGlobalBusinessUnit,
            'caseContactLastWorkDate': caseContactLastWorkDate,
            'caseSubcategory': caseSubcategory,
            'caseNumber': caseNumber,
            'caseID': caseID,
            'caseContactName': caseContactName,
            'caseContactEmpId': caseContactEmpId,
            'caseDescription': caseDescription,
            'caseCategory': caseCategory,
            'adGroupList': adGroupList,
            'PrimaryAffectedCIName': PrimaryAffectedCIName,
            'descriptionFields': description_fields
        }
        logger.info('Data processing completed successfully')
        return data

    except Exception as e:
        print(f"Error processing record: {e}")
        logger.error(f"Error processing record: {e}")
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        subject = 'Error in SalesForce Automation'
        body = f'{current_time}: Failed to get access token: {e}'
        sent_email(email_subject = subject, email_body = body)
        return None


def extract_description_fields(description):
    fields = {}
    try:
        lines = description.split('\n')
        for line in lines:
            key_value = re.split(r':\s*|\t', line, 1)
            if len(key_value) == 2:
                key, value = key_value
                fields[key.strip()] = value.strip()

    except Exception as e:
        print(f"Error extracting description fields: {e}")
        logger.error(f"Error extracting description fields: {e}")
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        subject = 'Error in SalesForce Automation'
        body = f'{current_time}: Failed to get access token: {e}'
        sent_email(email_subject = subject, email_body = body)

    return fields


def process_salesforce_data(data):
    try:
        results = []
        for i, record in enumerate(data.get('records', []), 1):
            result = extract_case_data(record)
            if result:
                results.append({'data': result})
        print(f"Total processed records {i}")
        logger.info(f"Total processed records {i}")
        return results

    except Exception as e:
        print(f"Error processing Salesforce data: {e}")
        logger.error(f"Error processing Salesforce data: {e}")
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        subject = 'Error in SalesForce Automation'
        body = f'{current_time}: Failed to get access token: {e}'
        sent_email(email_subject = subject, email_body = body)
        return []


def save_results_to_file(results, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        # print(f"Results saved to {filename}")
        logger.info(f"Results saved to {filename}")

    except Exception as e:
        # print(f"Error saving results to file: {e}")
        logger.error(f"Error saving results to file: {e}")
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        subject = 'Error in SalesForce Automation'
        body = f'{current_time}: Failed to get access token: {e}'
        sent_email(email_subject = subject, email_body = body)
