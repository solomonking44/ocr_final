from flask import Blueprint, render_template, flash, request, jsonify
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

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        document_data = [{'id': document.id, 'name': document.file, 'data': document.data} for document in current_user.document_id]
        # print(document_data)
        return render_template('index.html', user=current_user, documents=document_data)

    elif request.method == 'POST':
        file = request.files['file']
        print(file.filename)
        
        if not file:
            flash("Empty note!", category='error')
        else:
            if file.filename == '':
                flash("No file name", category="error")
            else:
                data = file.read()
                file.seek(0)
                file_extension = os.path.splitext(file.filename)[1].lower()

                if file_extension == '.pdf':
                    # Extract text from PDF
                    text = extract_text_from_pdf(data)
                    print(text)
                else:
                    # Save the file as usual
                    new_document = Document(file=file.filename, data=data, user_id=current_user.id)
                    db.session.add(new_document)
                    db.session.commit()
                    flash("Document Created!", category='success')

    else:
        return "Invalid method"
    
    return render_template('index.html', user=current_user)


def extract_text_from_pdf(data):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_filepath = temp_file.name
        temp_file.write(data)
    
    text = ""
    with pdfplumber.open(temp_filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    
    os.remove(temp_filepath)
    
    return text



@views.route('/delete-note', methods=['POST'])
def delete_note():
    data = json.loads(request.data)
    print(data)
    document_id = data['document_id']
    document = Note.query.get(document_id)
    if note:
        if document.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Document Deleted!", category='success')
            return jsonify({})
        else:
            flash("This is not your note", category="error")
    else:
        flash("Note does not exist", category="error")
    

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
        
        
    return text

# @views.route('/ocr/<int:document_id>', methods=['GET'])
# @login_required
# def ocr(document_id):