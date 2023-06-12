from flask import Blueprint, render_template, flash, request, redirect, url_for
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
from PIL import Image
from io import BytesIO
import csv

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        if request.method == 'GET':
            document_data = [{'id': document.id, 'name': document.file, 'data': document.data} for document in current_user.document_id]

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
    
    return redirect(url_for('views.home'))



@views.route('/delete-document/<int:document_id>', methods=['GET'])
def delete_document(document_id):
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
    return redirect(url_for('views.home'))
    


@views.route('/get_document_image/<int:document_id>', methods=['GET'])
@login_required
def get_document_image(document_id):
    document = Document.query.get_or_404(document_id)
    file_extension = os.path.splitext(document.file)[1].lower()

    if file_extension == '.pdf':
        # Extract a thumbnail from the first page of the PDF
        thumbnail = extract_pdf_thumbnail(document.data)
    elif file_extension in ['.jpg', '.jpeg', '.png']:
        # Read the image file
        thumbnail = Image.open(BytesIO(document.data))
    else:
        flash("Unsupported file format", category='error')
        return redirect(url_for('views.home'))
    
    # Create a thumbnail of the image
    thumbnail = create_thumbnail(thumbnail)
    
    # Save the thumbnail to a temporary file
    temp_dir = tempfile.gettempdir()
    temp_filename = f"thumbnail_{document_id}.jpg"
    temp_filepath = os.path.join(temp_dir, temp_filename)
    thumbnail.save(temp_filepath, "JPEG")
    
    # Serve the temporary thumbnail file
    return send_file(temp_filepath, mimetype='image/jpeg', as_attachment=False)

def extract_pdf_thumbnail(pdf_data):
    with pdfplumber.open(BytesIO(pdf_data)) as pdf:
        first_page = pdf.pages[0]
        image = first_page.to_image(resolution=72)  # Set the resolution as desired
        thumbnail = image.original.convert("RGB")
        return thumbnail

def create_thumbnail(image, max_size=(200, 200)):
    image.thumbnail(max_size)
    return image



@views.route('/ocr/<int:document_id>', methods=['GET'])
@login_required
def ocr(document_id):
    document = Document.query.get_or_404(document_id)
    file_extension = os.path.splitext(document.file)[1].lower()
    
    if file_extension == '.pdf':
        # Perform OCR on PDF using pdfplumber
        text = extract_text_from_pdf(document.data)
    elif file_extension in ['.jpg', '.jpeg', '.png']:
        # Perform OCR on image using pytesseract
        text = extract_text_from_image(document.data)
    else:
        flash("Unsupported file format", category='error')
        return redirect(url_for('views.home'))
    
    # Edit text in Zoho Writer
    url = "https://api.office-integrator.com/writer/officeapi/v1/documents?apikey=a962b1868966a007667c7c5f1bf74e72"
    payload = {
        'apikey': 'a962b1868966a007667c7c5f1bf74e72'
    }
    files = [
        ('document', (document.file.split('.', 1)[0], text))
    ]
    headers = {
        'Cookie': '051913c8ce=b2f3b97207f13ead5d1d3527e09c8d2a; JSESSIONID=686BD1B361CAD1F0E9EB3F754824651E; ZW_CSRF_TOKEN=437ff7a0-834d-48a7-9388-066a1a4c541b; _zcsr_tmp=437ff7a0-834d-48a7-9388-066a1a4c541b'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    json_data = json.loads(response.text)
    print(json_data['document_url'])
    return redirect(json_data['document_url'])

def extract_text_from_pdf(pdf_data):
    with tempfile.NamedTemporaryFile(delete=False) as temp_pdf_file:
        temp_pdf_file.write(pdf_data)
        temp_pdf_file.close()
        
        with pdfplumber.open(temp_pdf_file.name) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
                
        os.unlink(temp_pdf_file.name)
        
    return text

def extract_text_from_image(image_data):
    temp_dir = tempfile.gettempdir()
    temp_filename = "temp_image.jpg"
    temp_filepath = os.path.join(temp_dir, temp_filename)
    
    with open(temp_filepath, 'wb') as temp_image_file:
        temp_image_file.write(image_data)
        
    image = cv.imread(temp_filepath)
    text = pytesseract.image_to_string(image)
    
    os.unlink(temp_filepath)
    
    return text



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

    # Extract the headers from the first dictionary in the list
    filtered_data = []
    for item in data['result'][0]['prediction']:
        filtered_item = {item['label']: item['ocr_text']}
        filtered_data.append(filtered_item)

    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".csv") as file:
        csv_file = file.name

        # Get all unique labels from the filtered data
        labels = set(label for item in filtered_data for label in item.keys())

        # Write the data to the CSV file
        writer = csv.DictWriter(file, fieldnames=labels)
        writer.writeheader()
        writer.writerows(filtered_data)

    # # Read and print the contents of the CSV file
    with open(csv_file, 'r') as file:
        csv_contents = file.read()

    print("CSV file contents:")
    print(csv_contents)

    # # Edit CSV in Zoho Sheet
    document_name = document.file.split('.', 1)[0]

    url = "https://api.office-integrator.com/sheet/officeapi/v1/spreadsheet?apikey=a962b1868966a007667c7c5f1bf74e72"

    payload = {}
    files = [
        ('document', (f'{document_name}.csv', open(csv_file, 'rb')))
    ]
    headers = {
        'Cookie': 'JSESSIONID=6FB8F4F92D3AAF97A531DCB19C6D1362; _zcsr_tmp=06290659-5cf1-498a-9212-abd7535a4d40; c6d59bfa86=b4d10425a28875a69de70bd48446c54d; zscookcsr=06290659-5cf1-498a-9212-abd7535a4d40'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # print(response.text)

    try:
        data = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        print("Error: Invalid JSON response")
        print("Response content:")
        print(response.text)
        return response.text

    # print(data['document_url'])
    return redirect(data['document_url'])

