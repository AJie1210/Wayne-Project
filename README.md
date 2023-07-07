# Wayne Project
 
Line Notify:

import requests

url = "https://notify-api.line.me/api/notify"
token = 'H44jk8khEIz80QcCIoi7SXdCURr58ezeQFlUhYBqMJC'
message = '偵測到物體'
headers = {
    "Authorization": "Bearer " + token
}

if Motion == 1:
data = {
'message': message
}
data = requests.post(url, headers=headers, data=data)
