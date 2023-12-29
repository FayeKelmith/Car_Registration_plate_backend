import requests
import os
from db import get_number

def send_message(vehicle):
    print("vehicle",vehicle)
    url = 'https://www.fast2sms.com/dev/bulkV2'
    
    messages = {
   "warning": f"Please Mr/Mrs. {vehicle['owner']}, your vehicle with plate number {vehicle['plate']} has been detected in a no parking zone. Please move your vehicle immediately. Thank you.",
   "penalty" : f"Please Mr/Mrs. {vehicle['owner']}, your vehicle with plate number {vehicle['plate']} has been detected in a no parking zone. You have been fined {vehicle['charge']}. Please move your vehicle immediately. Thank you."
}

    

    payload = {
        'sender_id': 'TXTIND',
        'message': messages['penalty'] if vehicle['fined'] else messages['warning'],
        'route': 'q', 
        'language': 'english',
        'numbers': vehicle['contact']
    }
    headers = {
        'authorization': os.getenv('FAST2SMS_API'),
        'Content-Type':'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=payload, headers=headers)
    return response.text
