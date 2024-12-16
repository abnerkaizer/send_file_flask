from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from flask import request
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("KEY")
app.config['UPLOAD_FOLDER'] = os.getenv("FOLDER_PATH")


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET'])
def home():
    return '<h1>Flask Send File<h1>'

@app.route('/upload', methods=['GET','POST'])
def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        try:
            save_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config['UPLOAD_FOLDER'],
                secure_filename(file.filename)
            )
            
            file.save(save_path)
            flash("File has been uploaded successfully!", "success")
        except Exception as e:
            flash(f"Error during file upload: {str(e)}", "danger")
        return redirect(url_for('upload'))
    else:
        if form.errors:
            flash("Failed to upload file. Please try again.", "danger")
    return render_template('index.html', form=form)

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if 'file' not in request.files:
        return "No file part in the request.", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file.", 400

    try:
        save_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            app.config['UPLOAD_FOLDER'],
            secure_filename(file.filename)
        )
        file.save(save_path)
        return "File has been uploaded successfully!", 200
    except Exception as e:
        return f"Error during file upload: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
