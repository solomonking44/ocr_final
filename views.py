from flask import Blueprint, render_template, flash, request, redirect
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
    
    
    #edit text in zoho writer    
    url = "https://api.office-integrator.com/writer/officeapi/v1/documents?apikey=a962b1868966a007667c7c5f1bf74e72"

    payload = {
        'apikey': 'a962b1868966a007667c7c5f1bf74e72'
    }
    files=[
    ('document',('hello.docx',text))
    ]
    headers = {
    'Cookie': '051913c8ce=b2f3b97207f13ead5d1d3527e09c8d2a; JSESSIONID=686BD1B361CAD1F0E9EB3F754824651E; ZW_CSRF_TOKEN=437ff7a0-834d-48a7-9388-066a1a4c541b; _zcsr_tmp=437ff7a0-834d-48a7-9388-066a1a4c541b'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    json_data = json.loads(response.text)
    print(json_data['document_url'])
    return redirect(json_data['document_url'])


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
    
    url = 'https://app.nanonets.com/api/v2/OCR/Model/ceeebab1-5f48-4ce9-845e-066b81ce3d97/LabelFile/?async=false'

    data = {'file': open(temp_filepath, 'rb')}

    response = requests.post(url, auth=requests.auth.HTTPBasicAuth('78d1996a-9789-11ed-b6de-a693374d4922', ''), files=data)
    
    data = json.loads(response.text)

    filtered_data = []
    for item in data['result'][0]['prediction']:
        filtered_item = {item['label']: item['ocr_text']}
        filtered_data.append(filtered_item)
        

    print(filtered_data)
    return filtered_data
