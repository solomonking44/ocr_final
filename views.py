from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from .models import Document
from . import db
import json
# import os
import base64
import os
import tempfile
from flask import send_file
# import 
# import cv2 as cv

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        if request.method == 'GET':
            document_data = [{'id': document.id, 'name': document.file, 'data': document.data} for document in current_user.document_id]
            print(document_data)
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
                new_document = Document(file=file.filename, data=file.read(), user_id=current_user.id)
                db.session.add(new_document)
                db.session.commit()
                flash("Document Created!", category='success')  
    else:
        return "Invalid method"
    
    print(current_user)
    print(current_user.id)
    return render_template('index.html', user=current_user)



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
    
    
# @views.route('/get_document_image/<int:document_id>', methods=['GET'])
# @login_required
# def get_document_image(document_id):
#     document = Document.query.get_or_404(document_id)
#     encoded_image = base64.b64encode(document.data).decode('utf-8')
#     return f"data:image/jpeg;base64,{encoded_image}"

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