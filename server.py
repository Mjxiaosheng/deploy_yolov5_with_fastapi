#! /usr/bin/env python3
# *_* coding: utf-8 *_*
# @File  : server.py
# @Author: Frank1126lin
# @Date  : 2020/7/10

'''
使用FastAPI部署yolo5目标检测，通过fastapi存储传递的图片，在通过yolo5识别，然后将识别后的图片返回
'''

import os
import numpy as np
from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from predict import detect



app = FastAPI()
template = Jinja2Templates(directory="templates")

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    content = await file.read()
    file_name = file.filename
    dir_in = "./inference/input/"+file_name
    dir_out = "./inference/output"
    with open(dir_in, "wb") as f:
        f.write(content)
    detect(source=dir_in,out=dir_out)
    save_path = str(Path(dir_out) / file_name)
    # print(save_path)


    # with open("./inference/output")

    # assert
    # 如何使用yolov5直接读取传递的img对象？？？TODO

    return FileResponse(save_path)

@app.get("/")
async def index(request:Request):
    return template.TemplateResponse("index.html", {"request": request})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
