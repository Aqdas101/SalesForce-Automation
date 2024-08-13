import requests
import loggingConfig
from loggingConfig import logger
from emailSender import sent_email
from datetime import datetime
import os


def get_access_token(client_id, client_secret, username, password):
    try:
        url = "https://login.salesforce.com/services/oauth2/token"
        payload = {
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'password': password
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        # headers = {
        #     'Cookie': 'BrowserId=zoAZPhodEe-brLPJ5M2-FA; CookieConsentPolicy=0:0; LSKey-c$CookieConsentPolicy=0:0'
        # }

        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        print("Successfully fetched the Access Token")
        logger.info('Successfully fetched the Access Token')

        return response.json().get('access_token')

    except requests.exceptions.RequestException as e:
        print(f"Failed to get access token: {e}")
        logger.error(f"Failed to get access token: {e}")
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        subject = 'Error in SalesForce Automation'
        body = f'{current_time}: Failed to get access token: {e}'
        sent_email(email_subject = subject, email_body = body)
