from tokenApi import get_access_token
from salesforceApi import get_salesforce_data
from dataFormation import process_salesforce_data, save_results_to_file

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

import loggingconfig
import logging

from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

class SalesforceCredentials(BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str

    @classmethod
    def from_env(cls):
        return cls(
            client_id=os.getenv('CLIENT_ID'),
            client_secret=os.getenv('CLIENT_SECRET'),
            username=os.getenv('USERNAME'),
            password=os.getenv('PASSWORD')
        )
        

@app.post("/fetchData")
async def fetch_data(credentials: SalesforceCredentials):
    credentials = SalesforceCredentials.from_env()
    try:
        access_token = get_access_token(
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            username=credentials.username,
            password=credentials.password
        )
        
        if not access_token:
            logging.error('Failed to retrieve access token')
            raise HTTPException(status_code=500, detail="Failed to retrieve access token")

        
        data = get_salesforce_data(access_token)
        if not data:
            logging.error('Failed to fetch data from Salesforce')
            raise HTTPException(status_code=500, detail="Failed to fetch data from Salesforce")

        
        processed_data = process_salesforce_data(data)
        if not processed_data:
            logging.error('Failed to process Salesforce data')
            raise HTTPException(status_code=500, detail="Failed to process Salesforce data")

        filename = "processed_salesforce_data.json"
        save_results_to_file(processed_data, filename)

        return {
            "total_records": len(processed_data),
            "username": credentials.username,
            "message": "Successful",
            "data": processed_data,
            "file": filename
        }
    except Exception as e:
        logging.error(f"{str(e)}")
        raise HTTPException(status_code=500, detail=)

if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
