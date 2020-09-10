import requests

url = 'https://catbox.moe/user/api.php'
pl = {'reqtype': 'fileupload'}
payload = {'fileToUpload': open('brb.jpg', 'rb')}

print(requests.post(url, files=payload, data=pl).text)
