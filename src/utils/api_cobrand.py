import requests
import random
import json
from datetime import datetime

from faker import Faker

fake = Faker('id_ID')

def registerCobrand(branchId, produkName):
    payload = {
        "requestData": {
            "firstName": "MANA RIDHA",
            "lastName": fake.last_name_male(),
            "cardName": "MANA RIDHA " + fake.first_name_male(),
            "npwp": str(random.randint(10**14, 10**15 - 1)),
            "nik": str(random.randint(10**15, 10**16 - 1)),
            "birthPlace": "DKI JAKARTA",
            "birthDate": "1992-04-06",
            "addressLine1": "Menara Brilian Lt.28",
            "addressLine2": "Gatot Subroto",
            "addressLine3": "RT110 RW220, GROGOL PETAMBURAN",
            "sex": 1,
            "homeStatus": 1,
            "addressCity": "KOTA JAKARTA BARAT",
            "nationality": "WNI",
            "stayedSince": "03/10",
            "education": 6,
            "zipcode": "13960",
            "maritalStatus": 1,
            "motherName": fake.name_female(),
            "handPhoneNumber": "083490937151",
            "homePhoneArea": "021",
            "homePhoneNumber": "58078901",
            "email": fake.ascii_free_email(),
            "jobBidangUsaha": 80,
            "jobSubBidangUsaha": 8001,
            "jobCategory": 2,
            "jobStatus": 1,
            "totalEmployee": 4,
            "company": "PT.1919",
            "jobTitle": "APM",
            "workSince": "01/01",
            "officeAddress1": "Menara Sudirman LT 100",
            "officeAddress2": "Gatot Subroto",
            "officeAddress3": "KECAMATAN KOPO",
            "officeZipcode": "19110",
            "officeCity": "DKI JAKARTA",
            "officePhone": "021121232",
            "income": 9999999999999,
            "child": 0,
            "emergencyName": fake.first_name_male(),
            "emergencyRelation": 3,
            "emergencyAddress1": "Jl. Bidara Cina",
            "emergencyAddress2": "Jatinegara",
            "emergencyAddress3": "RT 76 RW 46, KECAMATAN TEBET",
            "emergencyCity": "KOTA JAKARTA SELATAN",
            "emergencyPhoneNumber": "0811233244",
            "productRequest": produkName,
            "billingCycle": 17,
            "cardDeliver": 1
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "branchId": str(branchId)
    }

    url = "http://172.24.141.35:1236/register" 

    response = requests.post(url, json=payload, headers=headers)
    responseData = response.text

    # Konversi string JSON ke dictionary
    response_data = json.loads(responseData)
    print(response_data)

    # Ambil responseCode dan briXkey
    response_code = response_data.get("responseCode")
    brixkey = response_data.get("responseData", {}).get("briXkey")

    # Validasi responseCode
    if response_code == "00":
        print("Response Code valid.")
        return brixkey
    else:
        print("Response Code tidak valid.")


def uploadDocuments(brixkey,branchId):
    headers = {
        "Content-Type": "application/json",
        "branchId": str(branchId)
    }

    doc_types = ["A", "P", "G", "D", "Z"]
    responses = {}
    
    url = "http://172.24.141.35:1236/document"
    
    for doc_type in doc_types:
        payload = {
            "requestData": {
                "briXkey": str(brixkey),
                "docType": doc_type,
                "fileExt": "pdf",
                "base64file": "data:image/jpeg;base64,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"
            }
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            responses[doc_type] = response.json()
            print(f"Response for docType {doc_type}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            responses[doc_type] = {"error": str(e)}
            print(f"Error sending request for docType {doc_type}: {e}")

    return responses

def checkNoApp(brixkeys):
    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
        "briXkey": str(brixkeys)
    }

    url = "http://172.24.141.35:1230//card/appstatus"

    response = requests.post(url, json=payload, headers=headers)
    responseData = response.text

    # Konversi string JSON ke dictionary
    response_data = json.loads(responseData)

    # Ambil responseCode
    response_code = response_data.get("responseCode")

    # Ambil appBarcode dari elemen pertama dalam responseData (jika ada)
    response_data_list = response_data.get("responseData", [])
    app_barcode = None
    if isinstance(response_data_list, list) and response_data_list:
        app_barcode = response_data_list[0].get("appBarcode")

    if response_code == "00":
        print("Response Code valid.")
        return app_barcode
    else:
        print("Response Code tidak valid.")
