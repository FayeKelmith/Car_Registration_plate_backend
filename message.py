import requests
import os

def send_message(numbers):
    url = 'https://www.fast2sms.com/dev/bulkV2'

    message = 'Just testing... sorry'


    payload = {
        'sender_id': 'TXTIND',
        'message': message,
        'route': 'q',
        'language': 'english',
        'numbers': numbers
    }
    headers = {
        'authorization': os.getenv('FAST2SMS_API'),
        'Content-Type':'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=payload, headers=headers)
    return response.text

# numbers = '7828645552,7761878881'
# print(send_message(numbers))