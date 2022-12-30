from flask import Blueprint, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from ..functions.functions import *

ALLOWED_EXTENSIONS = {'pdf'}

default_blueprint = Blueprint('default_blueprint', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@default_blueprint.route('/', methods=['GET', 'POST'])
def index():    
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            val = get_synthesis_pdf(file, filename)
            return render_template("index.html", test=val)
        
    return render_template("index.html", test='')

@default_blueprint.route('/treat-text', methods=['GET', 'POST'])
def execute_action():

    return ""