import os
import sys
import io
import base64
import tempfile
import shlex
import subprocess

import bottle
from bottle import default_app, route, get, post, static_file, request, view, url, template, redirect

# ~VIRTENV = os.environ.get('OPENSHIFT_PYTHON_DIR', '.') + '/virtenv/'
# ~virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
# ~PATH = os.path.abspath(os.environ.get('OPENSHIFT_HOMEDIR', '.'))
# ~PATH = os.path.abspath(os.path.join(VIRTENV))
PATH = os.path.abspath(os.environ.get('OPENSHIFT_REPO_DIR', '.'))
DATA_DIR = os.path.abspath(os.environ.get('OPENSHIFT_DATA_DIR', '.'))

bottle.TEMPLATE_PATH.insert(0, os.path.join(PATH, 'views'))

FFMPEG_DIR = os.path.join(PATH, 'ffmpeg/')

sys.path.append(FFMPEG_DIR)

FFMPEG_BIN = os.path.join(FFMPEG_DIR, 'ffmpeg')
FFPROBE_BIN = os.path.join(FFMPEG_DIR, 'ffprobe')
MK_SH = os.path.join(FFMPEG_DIR, 'mk.sh')
TMP_DIR = '/tmp'
WEBM_CACHE_DIR = os.path.join(DATA_DIR, 'mkwebm/webms/')
SIZE_X = 400


def do_upload():
    name = request.forms.name
    data = request.files.data
    if name and data and data.file:
        raw = data.file.read() # This is dangerous for big files
        filename = data.filename
        return "Hello %s! You uploaded %s (%d bytes)." % (name, filename, len(raw))
    return "You missed a field."


def upload_file(src, dest):
    try:
        if name and data and data.file:
            with open(dest, 'w') as f:
                f.write(src.read())
            return True
    except:
        return False

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static/')

@route('/')
@view('index')
def index():

    return dict()

@route('/mkwebm', method="POST")
# ~@view('mkwebm')
def mkwebm():

    params = request.params

    size_x = request.params.image_width or SIZE_X
    image_upload = request.files.get('image_file')
    audio_upload = request.files.get('audio_file')

    if not image_upload or not audio_upload:
        return False

    image_filename = image_upload.filename
    audio_filename = audio_upload.filename
    _, image_tmp_file_path = tempfile.mkstemp(suffix=image_filename, dir=TMP_DIR)
    _, audio_tmp_file_path = tempfile.mkstemp(suffix=audio_filename, dir=TMP_DIR)
    _, output_tmp_file_path = tempfile.mkstemp(suffix='.webm',dir=TMP_DIR)

    image_upload.save(image_tmp_file_path, overwrite=True)
    audio_upload.save(audio_tmp_file_path, overwrite=True)

    command = '{} "{}" "{}" {} "{}"'.format(MK_SH, image_tmp_file_path, audio_tmp_file_path, size_x, output_tmp_file_path)
    args = shlex.split(command)

    # ~res = subprocess.check_output(args)
    # ~print('ffmpeg output:\n',res, file=sys.stderr)
    proc = subprocess.Popen(args)
    proc.wait()

    basename = os.path.basename(output_tmp_file_path)

    output_file_path = os.path.join(WEBM_CACHE_DIR, basename)

    command = 'mv {} {}'.format(output_tmp_file_path, output_file_path)
    args = shlex.split(command)

    proc = subprocess.Popen(args)
    proc.wait()

    print('basename:\n', basename, file=sys.stderr)
    # ~return dict()
    # ~return static_file(basename, root=WEBM_CACHE_DIR)
    # ~return "<html><body>{}</body></html>".format(command)
    # ~return "<html><body>{}</body></html>".format(res)
    # ~return '<link href="{}" type="video/webm"/>'.format(url('webms', filename=basename))
    # ~return '/webms/{}'.format(basename)
    print('template:\n', template('<link href="{{ url("webms", filename=basename) }}" type="video/webm"/>', url=url, basename=basename))
    # ~return template('<html><body><link href="{{ url("webms", filename=basename) }}" type="video/webm"/></body></html>', url=url, basename=basename)
    redirect('/webms/{}'.format(basename))

@route('/dashboard')
@view('secure_page')
def show__page_dashboard():
    return dict(page='Dashboard', url=url)

@route('/webms/<filename:path>', name='webms')
def give_webm(filename):
    print('webm given')
    return static_file(filename, root=WEBM_CACHE_DIR)

application = default_app()
