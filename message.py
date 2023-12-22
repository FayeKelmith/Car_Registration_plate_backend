import requests

url = 'https://www.fast2sms.com/dev/bulkV2'

message = 'Apni gari hata bee chirkut .'

numbers = '7828645552,7761878881'

payload = {
    'sender_id': 'TXTIND',
    'message': message,
    'route': 'q',
    'language': 'english',
    'numbers': numbers
}
headers = {
    'authorization':'nkoh0KqbRguNyr2A8ea4CspcOziFEYXBMlV1QfxvjGZDw9ITStqb0ISkFTmhDPClvdGpAW3zHYufjner',
    'Content-Type':'application/x-www-form-urlencoded'
}

response = requests.post(url, data=payload, headers=headers)

print(response.text)