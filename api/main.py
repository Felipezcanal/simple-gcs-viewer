# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Felipe Zago Canal - felipe.z.canal@gmail.com
# Created at:  2022-07-20
# ---------------------------------------------------------------------------
""" Simple fastapi app to handle request """
import json
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import dotenv
import logging
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from Storage import Storage
import redis

origins = ['*']
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

storage = Storage()

cache = redis.Redis(host='gcs-viewer-redis', port=6379, db=0)

@app.post("/login")
async def login(data: Request):
    info = await data.json()
    try:
        email = info['email']
        password = info['password']
        if email != os.getenv('USER_EMAIL') or password != os.getenv('USER_PASSWORD'):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Successful login
        return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")



@app.get("/", include_in_schema=False)
def read_root():
    return {"msg": "Hello World"}

@app.post("/list")
async def list(data: Request):
    info = await data.json()
    response = cache.get('list_' + info['path'])
    if response is None:
        response = storage.list_dir(info['path'])
        # cache.set('list_' + info['path'], json.dumps(response), ex=60*10)
    else:
        response = json.loads(response)
    return response

@app.post("/get_signed_url")
async def signed_url(data: Request):
    info = await data.json()
    response = cache.get('signed_url_' + info['url'])
    if response is None:
        response = storage.get_signed_url(info['url'])
        cache.set('signed_url_' + info['url'], json.dumps(response), ex=60*10)
    else:
        response = json.loads(response)
    return response

@app.post("/download")
async def download(data: Request):
    info = await data.json()
    response = storage.download_files(info['paths'])
    return response

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format=f'%(asctime)s, %(name)s, %(levelname)s, %(message)s',
        filename='log.log',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    dotenv.load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT')))
