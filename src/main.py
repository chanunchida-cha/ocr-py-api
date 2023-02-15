import cv2
import uvicorn
import pytesseract
import numpy as np
import json
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

pytesseract.pytesseract.tesseract_cmd = r'../Tesseract-OCR/tesseract.exe'



app = FastAPI()

with open('drugName.json','r') as dataSet:
  data = json.load(dataSet)

pharmacies = data["drug_list"]


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def findPharmacy(imagePath, pharmacies):
    # Load the image
    # img = cv2.imread(imagePath)

    # Convert to grayscale
    gray = cv2.cvtColor(imagePath, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
 


    text = pytesseract.image_to_string(
        gray).lower().replace(r'[^\w\s]', '')
    foundPharmacy = ""
    for pharmacy in pharmacies:
        if pharmacy["drugName"].lower() in text:
            foundPharmacy = pharmacy["drugName"]
            break
        else :
            foundPharmacy = "กรุณาอัพโหลดภาพใหม่"
            

    return foundPharmacy

@app.post("/upload-file/")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    img = cv2.imdecode(np.fromstring(uploaded_file.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    print(img)
    result = findPharmacy(img,pharmacies)
    return {"result":result, "credit-by":"เพชรสุดหล่อ"}

# def main():
#     text = findPharmacy("./images/1.jpg", pharmacies)
#     print(text)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
