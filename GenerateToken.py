import requests

url = "https://accounts.spotify.com/api/token"
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

headers = {"Content-Type": "application/x-www-form-urlencoded"}
request_body = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "client_credentials"
}

response = requests.post(url, headers=headers, data=request_body)
print(response.json())