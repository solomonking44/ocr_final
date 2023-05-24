from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from .models import Document
from . import db
import json
import pytesseract
import base64
import os
import tempfile
from flask import send_file
import cv2 as cv
import pdfplumber
import requests

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        if request.method == 'GET':
            document_data = [{'id': document.id, 'name': document.file, 'data': document.data} for document in current_user.document_id]
            # print(document_data['name'])
            # print(document)
            return render_template('index.html', user=current_user, documents=document_data)

    elif request.method == 'POST':
        file = request.files['file']
        print(file.filename)
        
        if not file:
            flash("Empty Document!", category='error')
        else:
            if file.filename == '':
                flash("No file name", category="error")
            else:      
                new_document = Document(file=file.filename, data=file.read(), user_id=current_user.id)
                db.session.add(new_document)
                db.session.commit()
                flash("Document Created!", category='success')  
    else:
        return "Invalid method"
    
    print(current_user)
    print(current_user.id)
    return render_template('index.html', user=current_user)



@views.route('/delete-document/<int:document_id>', methods=['GET'])
def delete_document(document_id):
    # data = json.loads(request.data)
    # print(document_id)
    # document_id = data['document_id']
    document = Document.query.get(document_id)
    if document:
        if document.user_id == current_user.id:
            db.session.delete(document)
            db.session.commit()
            flash("Document Deleted!", category='success')
        else:
            flash("This is not your Document", category="error")
    else:
        flash("Document does not exist", category="error")
    return render_template('index.html', user=current_user)
    

@views.route('/get_document_image/<int:document_id>', methods=['GET'])
@login_required
def get_document_image(document_id):
    document = Document.query.get_or_404(document_id)

    # Save the image data to a temporary file
    temp_dir = tempfile.gettempdir()
    temp_filename = f"document_{document_id}.jpg"
    temp_filepath = os.path.join(temp_dir, temp_filename)
    with open(temp_filepath, 'wb') as file:
        file.write(document.data)
    

    # Serve the temporary image file
    return send_file(temp_filepath, mimetype='image/jpeg', as_attachment=False)

@views.route('/ocr/<int:document_id>', methods=['GET'])
@login_required
def ocr(document_id):
    document = Document.query.get_or_404(document_id)

    # Save the image data to a temporary file
    temp_dir = tempfile.gettempdir()
    temp_filename = f"document_{document_id}.jpg"
    temp_filepath = os.path.join(temp_dir, temp_filename)
    with open(temp_filepath, 'wb') as file:
        file.write(document.data)
        
        
    image = cv.imread(temp_filepath)
    
    text = pytesseract.image_to_string(image)
    
    #edit text
    url = "https://api.office-integrator.com/writer/officeapi/v1/documents"
    headers = {
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"
    }
    data = {
        "apikey": "a962b1868966a007667c7c5f1bf74e72",
        "document": text,
        "document_defaults": '{"track_changes":"disabled","language":"en-US"}',
        "editor_settings": '{"unit":"in","language":"en","view":"webview"}',
        "permissions": '{"document.export":true,"document.print":true,"document.edit":true,"review.changes.resolve":false,"review.comment":true,"collab.chat":true,"document.pausecollaboration":false,"document.fill":true}',
        "callback_settings": '{"save_format":"zdoc","save_url":"https://domain.com/save.php/"}',
        "document_info": '{"document_name":"New","document_id":1349}',
        "user_info": '{"user_id":"1973","display_name":"Ken"}',
        "ui_options": '{"save_button":"show","chat_panel":"show","dark_mode":"hide","file_menu":"show"}'
    }

    response = requests.post(url, headers=headers, files=data)

    print(response.status_code)
    print(response.json())
        
    # return text

@views.route('/socr/<int:document_id>', methods=['GET'])
@login_required
def socr(document_id):
    
    document = Document.query.get_or_404(document_id)

    # Save the image data to a temporary file
    temp_dir = tempfile.gettempdir()
    temp_filename = f"document_{document_id}.jpg"
    temp_filepath = os.path.join(temp_dir, temp_filename)
    with open(temp_filepath, 'wb') as file:
        file.write(document.data)
        
        
    image = cv.imread(temp_filepath)
    
    # text = pytesseract.image_to_string(image)
    
    url = 'https://app.nanonets.com/api/v2/OCR/Model/ceeebab1-5f48-4ce9-845e-066b81ce3d97/LabelFile/?async=false'

    data = {'file': open(temp_filepath, 'rb')}
    # print(data)

    response = requests.post(url, auth=requests.auth.HTTPBasicAuth('78d1996a-9789-11ed-b6de-a693374d4922', ''), files=data)

    # print(response.text)
    # response_data = response.text
    
    data = json.loads(response.text)

    filtered_data = []
    for item in data['result'][0]['prediction']:
        filtered_item = {item['label']: item['ocr_text']}
        filtered_data.append(filtered_item)
        

    # print(filtered_data)
    return filtered_data