import requests
import json

url = "https://api.office-integrator.com/writer/officeapi/v1/documents?apikey=a962b1868966a007667c7c5f1bf74e72"

payload = {
    'apikey': 'a962b1868966a007667c7c5f1bf74e72'
}
files=[
  ('document',('hello.docx','Hello world'))
]
headers = {
  'Cookie': '051913c8ce=b2f3b97207f13ead5d1d3527e09c8d2a; JSESSIONID=686BD1B361CAD1F0E9EB3F754824651E; ZW_CSRF_TOKEN=437ff7a0-834d-48a7-9388-066a1a4c541b; _zcsr_tmp=437ff7a0-834d-48a7-9388-066a1a4c541b'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

# print(response.text)
# print(response)

json_data = json.loads(response.text)
print(json_data['document_url'])