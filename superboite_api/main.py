
# TODO : Remove crentials from Docker
# TODO : Add the correct command line in make file


from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from googleapiclient.http import MediaIoBaseDownload
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import StreamingResponse
from typing import List
import io
import os
import json 
import requests


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Path to your service account JSON file
SERVICE_ACCOUNT_FILE = os.path.expanduser("~/.gcp/service-account-drive.json")

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

# Load credentials from the service account file
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the service
service = build('drive', 'v3', credentials=creds)

@app.get("/list_images", response_model=List[dict])
async def list_images():
    try:
        results = service.files().list(q="mimeType='image/jpeg'", pageSize=10).execute()
        files = results.get('files', [])
        return [{"ID": file['id'], "NAME": file['name']} for file in files]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_image/{file_id}")
async def get_image(file_id: str):
    try:
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fh.seek(0)
        return StreamingResponse(fh, media_type="image/jpeg")  # Adjust media type if needed
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post('/webhook')
async def webhook(request: Request):
    data = await request.json()
    if not data:
        return "Invalid data", 400

    # Extracting address components
    city = data.get('city', '')
    postal_code = data.get('postal_code', '')
    street = data.get('street', '')
    number = data.get('number', '')

    # Check if any essential address component is missing
    if not all([city, postal_code, street, number]):
        return "Incomplete address", 400

    # Constructing the address
    full_address = f"{number} {street}, {city} {postal_code}"

    # Google Maps Geocoding API
    api_key = "AIzaSyALT56yQPDKC-Ie6JE75l-tu00tdkCmIrA"
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": full_address, "key": api_key}
    response = requests.get(base_url, params=params)
    result = response.json()

    if result['status'] == 'OK':
        latitude = result['results'][0]['geometry']['location']['lat']
        longitude = result['results'][0]['geometry']['location']['lng']
        return {"latitude": latitude, "longitude": longitude}
    else:
        return "Geocoding failed", 500