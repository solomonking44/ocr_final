# import requests


# url = 'https://app.nanonets.com/api/v2/OCR/Model/ceeebab1-5f48-4ce9-845e-066b81ce3d97/LabelFile/?async=false'

#     data = {'files': open(temp_filepath, 'rb')}

#     response = requests.post(url, auth=requests.auth.HTTPBasicAuth('78d1996a-9789-11ed-b6de-a693374d4922', ''), files=data)
    
#     data = json.loads(response.text)

#     filtered_data = []
#     for item in data['result'][0]['prediction']:
#         filtered_item = {item['label']: item['ocr_text']}
#         filtered_data.append(filtered_item)