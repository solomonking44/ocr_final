import requests

url = 'https://writer.zoho.com/writer/officeapi/v1/document'
data = {
    'apikey': 'a962b1868966a007667c7c5f1bf74e72',
    'editor_settings': '{"unit":"in","language":"en","view":"pageview"}',
    'permissions': '{"document.export":true,"document.print":true,"document.edit":true,"review.changes.resolve":false,"review.comment":true,"collab.chat":true}',
    'callback_settings': '{"save_format":"docx","save_url":"http://localhost:5000/","context_info":"User or Doc Info"}',
    'document_info': '{"document_name":"Untitled Document","document_id":"567890123"}',
    'user_info': '{"user_id":"1000","display_name":"Alice"}',
    'document_defaults': '{"orientation":"portrait","paper_size":"Letter","font_name":"Lato","font_size":12,"track_changes":"disabled"}'
}

response = requests.post(url, data=data)
print(response.text)
