import os
from markupsafe import escape
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, send_file
from s3_demo import list_files, download_file, upload_file

app = Flask(__name__)

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#UPLOAD_FOLDER = "uploads"
BUCKET = "ecomidias-s3"
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpeg', 'jpg', 'mp3', 'mp4'}


def allowed_file(filename):
    return (('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS))


@app.route('/')
def entry_point():
    return 'Hello World!'

@app.route("/storage")
def storage():
    contents = list_files(BUCKET)
    return render_template('index.html', contents=contents)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        #f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        f.save(f.filename)
        #upload_file(f'uploads/{f.filename}', BUCKET)
        upload_file(f'{f.filename}', BUCKET)

        return redirect("/storage")

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)

if __name__ == '__main__':
    app.debug = True
    app.env = 'development'
    #app.run(host="0.0.0.0", port=80)
    app.run()
