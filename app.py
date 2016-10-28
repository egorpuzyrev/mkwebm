import gevent
from gevent import monkey


monkey.patch_all()


import os
import sys
import io
import base64
import tempfile
import shlex
import subprocess
import glob

import bottle
from bottle import default_app, route, get, post, static_file, request, view, url, template, redirect, response, request, run

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
def get_params():

    # ~params = request.params

    # ~size_x = request.forms.get('image_width') or SIZE_X
    try:
        size_x = request.forms.get('image_width', SIZE_X)
    except:
        yield template('<html><body>Error getting size_x</body></html>')
        return
    image_upload = request.files.get('image_file')
    audio_upload = request.files.get('audio_file')

    # ~if not image_upload or not audio_upload:
        # ~return False

    # ~conv(size_x, image_upload, audio_upload)

    image_filename = image_upload.filename
    audio_filename = audio_upload.filename
    _, image_tmp_file_path = tempfile.mkstemp(suffix=image_filename, dir=TMP_DIR)
    _, audio_tmp_file_path = tempfile.mkstemp(suffix=audio_filename, dir=TMP_DIR)
    # ~_, output_tmp_file_path = tempfile.mkstemp(suffix='.webm',dir=WEBM_CACHE_DIR)
    _, output_tmp_file_path = tempfile.mkstemp(suffix='.webm',dir=TMP_DIR)
    # ~_, new_output_tmp_file_path = tempfile.mkstemp(suffix='.webm',dir=WEBM_CACHE_DIR)

    basename = os.path.basename(output_tmp_file_path)
    new_output_tmp_file_path = os.path.join(WEBM_CACHE_DIR, basename)

    image_upload.save(image_tmp_file_path, overwrite=True)
    audio_upload.save(audio_tmp_file_path, overwrite=True)

    # ~command = '{} "{}" "{}" {} "{}"'.format(MK_SH, image_tmp_file_path, audio_tmp_file_path, size_x, output_tmp_file_path)
    command = """{} -hide_banner \
        -loglevel error \
        -loop 1 -i "{}" \
        -i "{}" \
        -shortest \
        -c:v libvpx \
        -c:a libopus \
        -threads 0 \
        -crf 33 -speed 2 \
        -tile-columns 6 -frame-parallel 1 -auto-alt-ref 1  -lag-in-frames 25 \
        -b:v 0 \
        -vf "scale={}:trunc(ow/a/2)*2" \
        -pix_fmt +yuv420p \
        -f webm \
        -y \
        "{}"
    """.format(FFMPEG_BIN, image_tmp_file_path, audio_tmp_file_path, size_x, output_tmp_file_path)
    args = shlex.split(command)

    print('start ffmpeg')
    yield template('wait.tpl', {'webm_file': '/webms/{}'.format(basename)})
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    print(out)
    # ~proc = subprocess.Popen(args)
    # ~proc.wait()

    command = 'mv -f "{}" "{}"'.format(output_tmp_file_path, new_output_tmp_file_path)
    args = shlex.split(command)
    proc = subprocess.Popen(args)
    proc.wait()


@route('/dashboard')
@view('secure_page')
def show__page_dashboard():
    return dict(page='Dashboard', url=url)

@route('/webms/<filename:path>', name='webms')
def give_webm(filename):
    print('webm given', os.path.join(WEBM_CACHE_DIR, filename))
    return static_file(filename, root=WEBM_CACHE_DIR)

@route('/webmslist')
@view('webmslist')
def show_webms_list():
    webms_list = [os.path.basename(i) for i in glob.glob(os.path.join(WEBM_CACHE_DIR, '*.webm'))]
    return {'webms_list': webms_list}


# ~run(reloader=True)
application = default_app()
# ~application.run(host=ip, port=port, server='gevent', reloader=True)
# ~application.run(host=ip, port=port, server='gevent')

from gevent.wsgi import WSGIServer

ip = os.environ.get('OPENSHIFT_PYTHON_IP', 'localhost')
port = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8051))
host_name = os.environ.get('OPENSHIFT_GEAR_DNS', '')

application.run(host=ip, port=port, server='gevent')
