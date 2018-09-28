import os
from flask import *
from flask import Flask, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_FILES_DEST'] = 'scribd'
#app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()

files = UploadSet(name='files', extensions= ('pdf','docs','docx'))
configure_uploads(app, (files))
patch_request_class(app)  # set maximum file size, default is 16MB


class UploadForm(FlaskForm):
    docc = FileField(validators=[FileAllowed(files, u'Documents only!'), FileRequired(u'File was empty!')])
    submit = SubmitField(u'Upload')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = files.save(form.docc.data)
        file_url = files.url(filename)
    else:
        file_url = None
    return render_template('index.html', form=form, file_url=file_url)


if __name__ == '__main__':
    app.run()