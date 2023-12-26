
# TODO : Remove crentials from Docker
# TODO : Add the correct command line in make file

from google.auth import default
from googleapiclient.discovery import build

from googleapiclient.http import MediaIoBaseDownload
import os
from fastapi import FastAPI, HTTPException, Request

from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import StreamingResponse
from typing import List
import io
import os
import json 
import requests
import chardet
from datetime import datetime




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

credentials, project = default()
service = build('drive', 'v3', credentials=credentials)

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

    city = data.get('city', '')
    postal_code = data.get('postal_code', '')
    street = data.get('street', '')
    number = data.get('number', '')
    if not all([city, postal_code, street, number]):
        return "Incomplete address", 400
    
    full_address = f"{number} {street}, {city} {postal_code}"
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



def get_google_sheet(sheet_id, range_name):
    serviceSheets = build('sheets', 'v4', credentials=credentials)
    sheet = serviceSheets.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values


def parse_data(sheet_data):
    headers = sheet_data[0]
    data = sheet_data[1:]
    lat_index = headers.index("Latitude")
    lon_index = headers.index("Longitude")
    formatted_data = []
    for row in data:
        if len(row) > max(lat_index, lon_index):
            entry = {
                "Name": row[0],
                "Latitude": row[lat_index],
                "Longitude": row[lon_index]
            }
            formatted_data.append(entry)

    return formatted_data


@app.get("/get_coords", response_class=JSONResponse)
def get_coords():
    sheet_id = "1d-R8Yai8mwCvXD4yDWPG4SE07ZtXfdLukcKQbL1BRN8"
    range_name = "data!A1:H" 
    data = get_google_sheet(sheet_id, range_name)
    results = parse_data(data)
    headers = {"Content-Type": "application/json; charset=utf-8"}
    return JSONResponse(content={"data": results}, headers=headers)


@app.post("/append_data")
async def append_data(request: Request):
    data = await request.json()
    SPREADSHEET_ID = "1WXLAnFffaXEUP5h215FYAMehz-3dGJaIcjG8tJ_B4jI"
    try:
        values = [[data["nom"], data["prenom"], data["phone"], data["email"], data["ville"], data["dispo"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")]]        
        service = build('sheets', 'v4', credentials=credentials)
        body = {'values': values}
        sheet = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range="Sheet1", valueInputOption="USER_ENTERED", body=body).execute()
        return {"message": "Data appended successfully", "updatedCells": sheet.get('updates').get('updatedCells')}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))