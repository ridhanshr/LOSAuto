import requests
import string
import random

from faker import Faker

fake = Faker('id_ID')

def updCycle(contract_numbers):
    url = "http://172.24.141.26:10001/way4appl/classifier/contracts"
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
                        "Data": {
                            "ContractNumber":cn,
                            "CustomerClassifiers": {
                                "Classifier": [
                                    {
                                        "Code": "BILL_DATE",
                                        "Value": "5",
                                        "ReasonDetails": "update Classifier"
                                    }
                                ]
                            }
                        }
                    }
                }
        
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            resp.raise_for_status()
            results.append(resp.json())
        except requests.Timeout:
            print(f"[updClassifier] Timeout for ContractNumber={cn}")
            results.append(None)
        except requests.HTTPError as http_err:
            print(f"[updClassifier] HTTP error for ContractNumber={cn}: {http_err} – {resp.text}")
            results.append(None)
        except requests.RequestException as err:
            print(f"[updClassifier] Request exception for ContractNumber={cn}: {err}")
            results.append(None)
    
    return results

# Contoh pemakaian:
if __name__ == "__main__":
    contracts = [
    '5534790300000858',
    '5534790500000856',
    '5534790200000859',
    '5534790100000850',
    '6189500100000495'

]

    responses = updCycle(contracts)
    for cn, res in zip(contracts, responses):
        print(f"{cn} → {res}")  
