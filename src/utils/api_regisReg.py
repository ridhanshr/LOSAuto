import requests
import random
import json
from card_generator import generate_cards
from datetime import datetime
from faker import Faker

fake = Faker('id_ID')

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

def regisClientRegular(ClientNumber):
    """Register a regular client."""
    client_full = {
        "ClientInfo": {
            "ClientNumber": ClientNumber,
            "RegNumber": str(random.randint(10**15, 10**16 - 1)),
            "RegNumberDetails": "REGULAR" + str(random.randint(10**7, 10**8 - 1)),
            "ShortName": fake.first_name().upper(),
            "SocialNumber": "CIF" + str(random.randint(10**7, 10**8 - 1)),
            "TaxpayerIdentifier": str(random.randint(10**14, 10**15 - 1)),
            "TaxPosition": "EDM" + str(random.randint(10**7, 10**8 - 1)),
            "Title": "MR",
            "FirstName": fake.first_name().upper(),
            "LastName": fake.last_name().upper(),
            "SecurityName": fake.first_name_female().upper(),
            "Country": "IDN",
            "MaritalStatus": "M",
            "Position": "WIRAUSAHA",
            "CompanyName": "WIRA USAHAWAN INC",
            "BirthDate": fake.date_of_birth(minimum_age=18, maximum_age=65).strftime("%Y-%m-%d"),
            "BirthPlace": "Jakarta",
            "Gender": "Male"
        },
        "DateOpen": current_date,
        "PlasticInfo": {
            "Title": "MR",
            "FirstName": fake.first_name().upper(),
            "LastName": fake.last_name().upper()
        },
        "AddInfo": {
            "AddInfo01": "MEMO1=BUSINESS CARD AERO SYSTEM INDONESIA;MEMO2=;APP_NO=null;EU_EDU=04;",
            "AddInfo02": "EU_NBR_OF_DEPS=02;EU_PER_OCCPN=3000;"
        },
        "SubAppl": {
            "CustomerClassifiers": {
                "Classifier": [
                    {"Code": "STMT_TYPE", "Value": "2"},
                    {"Code": "CARD_DLVR_ADDR", "Value": "1"},
                    {"Code": "STMT_DLVR_ADDR", "Value": "1"}
                ]
            },
            "IssuingContracts": [
                {
                    "ContractIDT": {"RBSNumber": "0"},
                    "Product": {
                        "ProductCode1": "CL_I"
                    },
                    "DateOpen": current_date,
                    "CreditLimit": {
                        "FinanceLimit": {
                            "Amount": "150000000",
                            "Currency": "IDR"
                        },
                        "ReasonDetails": "Credit Line"
                    },
                    "SubAppl": {
                        "SubAddress": [
                            {
                                "AddressType": "PHS_ADDR",
                                "City": "Jakarta",
                                "EMail": "clientacq@gmail.com",
                                "AddressLine1": "Jl. CL no.92",
                                "AddressLine2": "Jatinegari",
                                "AddressLine3": "Bidara Cini",
                                "PostalCode": "21232",
                                "Country": "IDN",
                                "PhoneList": {
                                    "Phone": [
                                        {"PhoneType": "Mobile", "PhoneNumber": "089672202323"},
                                        {"PhoneType": "Home", "PhoneNumber": "021891223"},
                                        {"PhoneType": "Work", "PhoneNumber": "0218012224"}
                                    ]
                                }
                            },
                            {
                                "AddressType": "WRK_ADDR",
                                "City": "Jakarta",
                                "EMail": "workemailacq@gmail.com",
                                "AddressLine1": "Jl. Work no.18",
                                "AddressLine2": "Bekasi",
                                "AddressLine3": "Bidara Cini",
                                "PostalCode": "21237",
                                "Country": "IDN",
                                "PhoneList": {
                                    "Phone": [
                                        {"PhoneType": "Mobile", "PhoneNumber": "089672282323"},
                                        {"PhoneType": "Home", "PhoneNumber": "021801229"},
                                        {"PhoneType": "Work", "PhoneNumber": "021801229"}
                                    ]
                                }
                            }
                        ],
                        "CustomerClassifiers": {
                            "Classifier": [
                                {"Code": "CH_MAIN_ADDR", "Value": "OFC"}
                            ]
                        }
                    }
                }
            ]
        }
    }
    
    payload = {
        "SourceApp": "LOS0",
        "Application": {
            "Data": {
                "ClientFull": client_full
            }
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "MsgId": str(random.randint(10**9, 10**10 - 1))
    }

    url = "http://172.24.141.26:10001/way4appl/typeClient/clients"
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    print(f"\n--- Debug Info Regular Client Registration ---")
    print(f"Status Code: {response.status_code}")
    
    return response.json()

def regisClientCorporate(ClientNumber):
    """Register a corporate client."""
    client_full_data = {
        "ClientInfo": {
            "ClientNumber": ClientNumber,
            "RegNumber": str(random.randint(10**15, 10**16 - 1)),
            "RegNumberDetails": str(random.randint(10**7, 10**8 - 1)),
            "ShortName": fake.first_name().upper(),
            "SocialNumber": "CIF" + str(random.randint(10**7, 10**8 - 1)),
            "TaxpayerIdentifier": str(random.randint(10**14, 10**15 - 1)),
            "TaxPosition": "EDM" + str(random.randint(10**7, 10**8 - 1)),
            "Title": "MR",
            "FirstName": fake.first_name().upper(),
            "LastName": fake.last_name().upper(),
            "Country": "IDN",
            "MaritalStatus": "M",
            "CompanyName": "PT SUKSES ABADI",
            "BirthDate": "1967-08-15",
            "BirthPlace": "Jakarta",
            "Gender": "Male"
        },
        "DateOpen": current_date,
        "AddInfo": {
            "AddInfo01": "MEMO1=BUSINESS CARD AGRONIAGA;MEMO2=;APP_NO=null;EU_EDU=04;",
            "AddInfo02": "EU_NBR_OF_DEPS=02;EU_PER_OCCPN=3000;"
        },
        "SubAppl": {
            "CustomerClassifiers": {
                "Classifier": [
                    {"Code": "STMT_TYPE", "Value": "0"},
                    {"Code": "CARD_DLVR_ADDR", "Value": "0"},
                    {"Code": "STMT_DLVR_ADDR", "Value": "0"}
                ]
            },
            "IssuingContracts": [
                {
                    "ContractIDT": {"RBSNumber": "0"},
                    "Product": {
                        "ProductCode1": "CCL_I"
                    },
                    "DateOpen": current_date,
                    "CreditLimit": {
                        "FinanceLimit": {
                            "Amount": "30000000000",
                            "Currency": "IDR"
                        },
                        "ReasonDetails": "Credit Line"
                    },
                    "SubAppl": {
                        "SubAddress": [
                            {
                                "AddressType": "PHS_ADDR",
                                "City": "Jakarta",
                                "EMail": fake.ascii_free_email(),
                                "AddressLine1": "JL. Tebit Birat VIII No. 316",
                                "AddressLine2": "Kelurahan Tebit Birat",
                                "AddressLine3": "Kecamatan Tebit",
                                "PostalCode": "12819",
                                "Country": "IDN",
                                "PhoneList": {
                                    "Phone": [
                                        {"PhoneType": "Mobile", "PhoneNumber": "08528271123"},
                                        {"PhoneType": "Home", "PhoneNumber": "08528279229"},
                                        {"PhoneType": "Work", "PhoneNumber": "02128271123"}
                                    ]
                                }
                            },
                            {
                                "AddressType": "WRK_ADDR",
                                "City": "Jakarta",
                                "EMail": fake.ascii_free_email(),
                                "AddressLine1": "Jl. Gatit Subrito No. 177A",
                                "AddressLine2": "Kelurahan Menteng Dalem",
                                "AddressLine3": "Kecamatan Tebit",
                                "PostalCode": "12871",
                                "Country": "IDN",
                                "PhoneList": {
                                    "Phone": [
                                        {"PhoneType": "Mobile", "PhoneNumber": "08528276423"},
                                        {"PhoneType": "Home", "PhoneNumber": "08528278323"},
                                        {"PhoneType": "Work", "PhoneNumber": "02128276323"}
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
    
    # Ensure ClientType is the first key
    client_full = {"ClientType": "CR", **client_full_data}
    
    payload = {
        "SourceApp": "LOS0",
        "Application": {
            "Data": {
                "ClientFull": client_full
            }
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "MsgId": str(random.randint(10**9, 10**10 - 1))
    }

    url = "http://172.24.141.26:10001/way4appl/typeClient/clients"
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    print(f"\n--- Debug Info Corporate Client Registration ---")
    print(f"Status Code: {response.status_code}")
    print("request payload:", json.dumps(payload, indent=4))
    
    return response.json()

def regisCardRegular(cardNumber, ProductCode1, ProductCode2):
    """Register a regular card."""
    sub_contract_subappl = {
        # "SubProduceCard": {
        #     "ProductionEvent": "NVCRD"
        # },
        "CustomerClassifiers": {
            "Classifier": [
                {"Code": "WAIVE_ANN_FEE", "Value": "0"},
                {"Code": "CRD_TYP", "Value": "PHY"},
                {"Code": "ISS_PRTY", "Value": "Y"}
            ]
        }
    }

    payload = {
        "SourceApp": "LOS0",
        "Application": {
            "ClientNumber": cardNumber,
            "Data": {
                "Contract": {
                    "ContractIDT": {
                        "RBSNumber": "0"
                    },
                    "Product": {
                        "ProductCode1": ProductCode1
                    },
                    "DateOpen": current_date,
                    "LiabContract": {
                        "LiabCategory": "CheckBalance",
                        "ContractIDT": {
                            "ContractNumber": "002-P-CL" + cardNumber
                        }
                    },
                    "CreditLimit": {
                        "FinanceLimit": {
                            "Amount": "150000000",
                            "Currency": "IDR"
                        },
                        "ReasonDetails": "Credit"
                    },
                    "SubAppl": {
                        "CustomerClassifiers": {
                            "Classifier": [
                                {"Code": "BLK_CD", "Value": "N"},
                                {"Code": "BILL_DATE", "Value": "30"},
                                {"Code": "POT_CD", "Value": "01"}
                            ]
                        },
                        "SubContracts": [
                            {
                                "ContractIDT": {
                                    "ContractNumber": cardNumber
                                },
                                "Product": {
                                    "ProductCode1": ProductCode2
                                },
                                "PlasticInfo": {
                                    "Title": "MR",
                                    "LastName": fake.first_name().upper()
                                },
                                "SubAppl": sub_contract_subappl
                            }
                        ]
                    }
                }
            }
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "MsgId": str(random.randint(10**9, 10**10 - 1))
    }

    url = "http://172.24.141.26:10001/way4appl/typeContract/clients"   
    print("request", payload)
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    print(f"\n--- Debug Info Regular Card Registration ---")
    print(f"Status Code: {response.status_code}")

    return response.json()

def regisCardCorporate(cardNumber, ProductCode1, ProductCode2):
    """Register a corporate card."""
    sub_contract_subappl = {
        "SubAddress": [
            {
                "AddressType": "PHS_ADDR",
                "City": "Jakarta",
                "EMail": "uat1140@gmail.com",
                "AddressLine1": "JL. Tebet Barat VIII No. 3 16",
                "AddressLine2": "Kelurahan Tebet Barat",
                "AddressLine3": "Kecamatan Tebet",
                "PostalCode": "12810",
                "Country": "IDN",
                "PhoneList": {
                    "Phone": [
                        {"PhoneType": "Mobile", "PhoneNumber": "089612212323"},
                        {"PhoneType": "Home", "PhoneNumber": "0218012281"},
                        {"PhoneType": "Phone", "PhoneNumber": "0218012223"}
                    ]
                }
            },
            {
                "AddressType": "WRK_ADDR",
                "City": "Jakarta",
                "EMail": "uat1140@mail.com",
                "AddressLine1": "Jl. Gatot Subroto No. 177A",
                "AddressLine2": "Kelurahan Menteng Dalam",
                "AddressLine3": "Kecamatan Tebet",
                "PostalCode": "12870",
                "Country": "IDN",
                "PhoneList": {
                    "Phone": [
                        {"PhoneType": "Mobile", "PhoneNumber": "089672222323"},
                        {"PhoneType": "Home", "PhoneNumber": "0218012213"}
                    ]
                }
            }
        ],
        "CustomerClassifiers": {
            "Classifier": [
                {"Code": "WAIVE_ANN_FEE", "Value": "0"},
                {"Code": "CRD_TYP", "Value": "PHY"},
                {"Code": "ISS_PRTY", "Value": "Y"}
            ]
        }
    }

    payload = {
        "SourceApp": "LOS0",
        "Application": {
            "ClientType": "CR",
            "ClientNumber": cardNumber,
            "Data": {
                "Contract": {
                    "ContractIDT": {
                        "RBSNumber": "0"
                    },
                    "Product": {
                        "ProductCode1": ProductCode1
                    },
                    "DateOpen": current_date,
                    "LiabContract": {
                        "LiabCategory": "CheckBalance",
                        "ContractIDT": {
                            "ContractNumber": "002-C-CL" + cardNumber
                        }
                    },
                    "CreditLimit": {
                        "FinanceLimit": {
                            "Amount": "150000000",
                            "Currency": "IDR"
                        },
                        "ReasonDetails": "Credit"
                    },
                    "SubAppl": {
                        "CustomerClassifiers": {
                            "Classifier": [
                                {"Code": "BLK_CD", "Value": "N"},
                                {"Code": "BILL_DATE", "Value": "30"},
                                {"Code": "POT_CD", "Value": "01"}
                            ]
                        },
                        "SubContracts": [
                            {
                                "ContractIDT": {
                                    "ContractNumber": cardNumber
                                },
                                "Product": {
                                    "ProductCode1": ProductCode2
                                },
                                "PlasticInfo": {
                                    "Title": "MR",
                                    "LastName": fake.first_name().upper()
                                },
                                "SubAppl": sub_contract_subappl
                            }
                        ]
                    }
                }
            }
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "MsgId": str(random.randint(10**9, 10**10 - 1))
    }

    url = "http://172.24.141.26:10001/way4appl/typeContract/clients"   
    # print("request", payload)
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    print(f"\n--- Debug Info Corporate Card Registration ---")
    print(f"Status Code: {response.status_code}")

    return response.json()

# Example
if __name__ == "__main__":
    cards = generate_cards(prefix="61895101", start_number=9382, count=2)
    for card in cards:
        print(f"--- Processing Regular Card: {card['card_number']} ---")
        regisClientRegular(card['card_number'])
        regisCardRegular(card['card_number'], "GPNRC_I", "GPNRC_C_KKST_M")
        print("Regular Card Registered\n")

    # cards_corp = generate_cards(prefix="61895001", start_number=9169, count=2)
    # for card in cards_corp:
    #     print(f"--- Processing Corporate Card: {card['card_number']} ---")
    #     regisClientCorporate(card['card_number'])
    #     regisCardCorporate(card['card_number'], "GPNCC_I", "GPNCC_C_KKPD")
    #     print("Corporate Card Registered\n")