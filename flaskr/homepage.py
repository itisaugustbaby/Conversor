from flask import current_app, request, Blueprint, render_template, send_file, redirect, url_for, flash
import os, io, mimetypes
from pytube import YouTube
import functools
#https://www.youtube.com/watch?v=R6F9BzOeo2Y queima quengaral de teste
bp = Blueprint('homepage',__name__)


        
def get_stream(yt_url,download_type):
    yt=YouTube(yt_url)
    if download_type == 'video':
        stream=yt.streams.filter(progressive=True).get_highest_resolution()
        return stream
    elif download_type == 'audio':
        stream = yt.streams.filter(type='audio').last()
        return stream
    else:
        raise ValueError('Valor inválido')
def checa_url(url):
    try:
        YouTube(url).check_availability()
    except:
        return 'Url ou Vídeo Indisponível.'
def download_stream(stream,tipo):
    extensao = '.mp4' if tipo == 'video' else '.mp3'
    stream.download('flaskr\downloads','download'+extensao)
    return extensao
@bp.route('/',methods=('POST','GET'))
def homepage():
    if request.method == 'POST':
        url = request.form['url']
        tipo = request.form['type']
        error = checa_url(url)
        if error is None:
            stream=get_stream(url,tipo)
            extensao=download_stream(stream,tipo)
            filename=f'download{extensao}'
            return redirect(url_for('homepage.download_file',file=filename))
        else:
            flash(error)
    return render_template('index.html')

@bp.route('/uploads/<file>')
def download_file(file):
    root, upload_path = current_app.root_path, current_app.config['UPLOAD_FOLDER']
    bytes_data = io.BytesIO()
    with open(os.path.join(root,upload_path,file),'rb') as d:
        bytes_data.write(d.read())
    
    bytes_data.seek(0)
    os.remove(os.path.join(root,upload_path,file))
    my_response = send_file(bytes_data,
            mimetype=mimetypes.guess_type(file)[0],as_attachment=True, download_name=file)
    return my_response


