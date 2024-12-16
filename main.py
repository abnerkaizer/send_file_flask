from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
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

@app.route('/uploud', methods=['GET', 'POST'])
def uploud():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        try:
            # Caminho completo para salvar o arquivo
            save_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config['UPLOAD_FOLDER'],
                secure_filename(file.filename)
            )
            
            # Tenta salvar o arquivo
            file.save(save_path)
            flash("File has been uploaded successfully!", "success")
        except Exception as e:
            flash(f"Error during file upload: {str(e)}", "danger")
        return redirect(url_for('uploud'))
    else:
        if form.errors:
            flash("Failed to upload file. Please try again.", "danger")
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
