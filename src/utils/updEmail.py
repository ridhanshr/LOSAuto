import requests
import string
import random

from faker import Faker

fake = Faker('id_ID')

def updateEmail(contract_numbers):
    # Generate msgID 15 karakter alfanumerik sekali untuk keseluruhan batch
    
    url = "http://172.24.141.26:10001/way4appl/address/contracts"
    results = []
    for cn in contract_numbers:
        charset = string.ascii_letters + string.digits
        msg_id = ''.join(random.choices(charset, k=15))

        headers = {
            "Content-Type": "application/json",
            "msgID": msg_id
        }
        
        payload = {
                    "SourceApp": "BCCM",
                    "Application": {
                        "ContractNumber": "002-P-CL" + cn,
                        "Data": {
                            "Address": {
                                "AddressType": "PHS_ADDR",
                                "EMail": "ryan.stiawann@gmail.com"
                            }
                        }
                    }
                }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            resp.raise_for_status()
            results.append(resp.json())
        except requests.Timeout:
            print(f"[registerCobrand] Timeout for ContractNumber={cn}")
            results.append(None)
        except requests.HTTPError as http_err:
            print(f"[registerCobrand] HTTP error for ContractNumber={cn}: {http_err} – {resp.text}")
            results.append(None)
        except requests.RequestException as err:
            print(f"[registerCobrand] Request exception for ContractNumber={cn}: {err}")
            results.append(None)
    
    return results

# Contoh pemakaian:
if __name__ == "__main__":
    contracts = [
    '1895990202248207',
    '1895990202248504',
    '1895990202248108',
    '1895990202248405',
    '1895990202248306'
    ]

    responses = updateEmail(contracts)
    for cn, res in zip(contracts, responses):
        print(f"{cn} → {res}")
