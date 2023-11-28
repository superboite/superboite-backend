# from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google.auth import compute_engine

from googleapiclient.http import MediaIoBaseDownload
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
import io

app = FastAPI()

SCOPES = ['https://www.googleapis.com/auth/drive']
creds = compute_engine.Credentials(scopes=SCOPES)
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
