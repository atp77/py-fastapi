import os
import shutil
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

router = APIRouter()

config = {
	'WORK_DIR':'/tmp/'
}

### Heart beat check
@router.get("/ping")
async def ping():
    return {"ping": "Heartbeat Check1!"}

## API endpoint to upload file Serves HTML Form
@router.get("/fileupload")
async def main():
    content = """
        <body>
        <form action="/upload/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        </body>
	"""
    return HTMLResponse(content=content)


#### Upload endpoint called by the fileUpload method upon form submission
@router.post("/upload")
async def create_upload_files(files: List[UploadFile] = File(...)):
    WORK_DIR = Path(config.get('WORK_DIR'))
    REQUEST_ID = Path(str(uuid.uuid4())[:8])
    WORKSPACE = WORK_DIR / REQUEST_ID
    if not os.path.exists(WORKSPACE):
        # recursively create workdir/unique_id
        os.makedirs(WORKSPACE)
    # iterate through all uploaded files
    for file in files:
        FILE_PATH = Path(file.filename)
        WRITE_PATH = WORKSPACE / FILE_PATH
        with open(str(WRITE_PATH) ,'wb') as myfile:
            contents = await file.read()
            myfile.write(contents)
    #return local file paths
    return {"file_paths": [str(WORKSPACE)+'/'+file.filename for file in files]}
