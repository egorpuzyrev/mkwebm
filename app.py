
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
import time

import bottle
from bottle import default_app, route, get, post, static_file, request, view, url, template, redirect, response, request, run

# import asyncio

# ~VIRTENV = os.environ.get('OPENSHIFT_PYTHON_DIR', '.') + '/virtenv/'
# ~virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
# ~PATH = os.path.abspath(os.environ.get('OPENSHIFT_HOMEDIR', '.'))
# ~PATH = os.path.abspath(os.path.join(VIRTENV))
PATH = os.path.abspath(os.environ.get('OPENSHIFT_REPO_DIR', '.'))
DATA_DIR = os.path.abspath(os.environ.get('OPENSHIFT_DATA_DIR', '.'))

SCRIPTS_DIR = os.path.join(PATH, 'scripts/')
ANIM_SH = os.path.join(SCRIPTS_DIR, 'anim.sh')
STATIC_SH = os.path.join(SCRIPTS_DIR, 'static.sh')
FREE_SPACE_SH = os.path.join(SCRIPTS_DIR, 'free_space.sh')

bottle.TEMPLATE_PATH.insert(0, os.path.join(PATH, 'views'))

FFMPEG_DIR = os.path.join(PATH, 'ffmpeg/')

sys.path.append(FFMPEG_DIR)
sys.path.append(SCRIPTS_DIR)

FFMPEG_BIN = os.path.join(FFMPEG_DIR, 'ffmpeg')
FFPROBE_BIN = os.path.join(FFMPEG_DIR, 'ffprobe')
MK_SH = os.path.join(FFMPEG_DIR, 'mk.sh')
TMP_DIR = os.path.abspath(os.environ.get('OPENSHIFT_TMP_DIR', '.'))
WEBM_CACHE_DIR = os.path.join(DATA_DIR, 'mkwebm/webms/')
SIZE_X = 400
# ~MAX_SIZE_KB = 30720
MAX_SIZE_KB = 102400

GIF_LOOP_OPTIONS = """-ignore_loop 0"""
STATIC_LOOP_OPTIONS = """-r 1 -loop 1"""

LOG_FILE = os.path.join(DATA_DIR, 'log.txt')
SCRIPTS_LOG_FILE = os.path.join(DATA_DIR, 'scripts_log.txt')

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
    with open('counter.txt') as f:
        views_couter = f.read()

    return {'mkwebm_views_counter': views_couter}

@route('/mkwebm', method="POST")
# ~@view('mkwebm')
def get_params():
    begin = time.time()
    # ~params = request.params
    scripts_log_file = open(SCRIPTS_LOG_FILE, 'a')

    # ~size_x = request.forms.get('image_width') or SIZE_X
    try:
        size_x = request.forms.get('image_width', SIZE_X)
    except:
        yield template('<html><body>Error getting size_x</body></html>')
        return
    image_upload = request.files.get('image_file')
    audio_upload = request.files.get('audio_file')
    total_size_kb = int(float(request.forms.get('total_size_kb', MAX_SIZE_KB)))
    # ~if not image_upload or not audio_upload:
        # ~return False

    command = '{} {}'.format(FREE_SPACE_SH, total_size_kb)
    # ~command = '{} {} &>> {SCRIPTS_LOG_FILE}'.format(FREE_SPACE_SH, total_size_kb, SCRIPTS_LOG_FILE=SCRIPTS_LOG_FILE)
    args = shlex.split(command)
    # ~proc = subprocess.Popen(args)
    proc = subprocess.Popen(args, stdout=scripts_log_file, stderr=scripts_log_file)
    proc.wait()


    image_filename = (image_upload.raw_filename)#.encode('utf-8')
    audio_filename = (audio_upload.raw_filename)#.encode('utf-8')
    _, image_tmp_file_path = tempfile.mkstemp(suffix=image_filename, dir=TMP_DIR)
    _, audio_tmp_file_path = tempfile.mkstemp(suffix=audio_filename, dir=TMP_DIR)


    if image_filename.lower().endswith('.gif'):
        script_name = ANIM_SH
        _, output_tmp_file_path = tempfile.mkstemp(suffix=(os.path.splitext(audio_filename)[0]+'.mp4'),dir=TMP_DIR)
    else:
        script_name = STATIC_SH
        _, output_tmp_file_path = tempfile.mkstemp(suffix=(os.path.splitext(audio_filename)[0]+'.webm'),dir=TMP_DIR)

    basename = os.path.basename(output_tmp_file_path)
    # ~print("basename: ", basename, file=sys.stderr)
    new_output_tmp_file_path = os.path.join(WEBM_CACHE_DIR, basename)
    # ~print("new_output_tmp_file_path: ", basename, file=sys.stderr)

    image_upload.save(image_tmp_file_path, overwrite=True)
    audio_upload.save(audio_tmp_file_path, overwrite=True)

    yield template('wait.tpl', {'webm_file': '/webms/{}'.format(basename)})

    command = '{script_name} "{image_file}" "{audio_file}" "{output_file}" "{new_output_tmp_file_path}" {size_x}'.format(
        script_name=script_name,
        image_file=image_tmp_file_path,
        audio_file=audio_tmp_file_path,
        output_file=output_tmp_file_path,
        new_output_tmp_file_path=new_output_tmp_file_path,
        size_x=size_x
    )
    # ~command = '{script_name} "{image_file}" "{audio_file}" "{output_file}" "new_output_tmp_file_path" {size_x} &>> {SCRIPTS_LOG_FILE}'.format(
        # ~script_name=script_name,
        # ~image_file=image_tmp_file_path,
        # ~audio_file=audio_tmp_file_path,
        # ~output_file=output_tmp_file_path,
        # ~new_output_tmp_file_path=new_output_tmp_file_path,
        # ~size_x=size_x,
        # ~SCRIPTS_LOG_FILE=SCRIPTS_LOG_FILE
    # ~)

    # ~command = '{} "{}" "{}" {} "{}"'.format(MK_SH, image_tmp_file_path, audio_tmp_file_path, size_x, output_tmp_file_path)
    # ~command = """{ffmpeg} -hide_banner \
        # ~-loglevel error \
        # ~{loop_options} \
        # ~-i "{image_file}" \
        # ~-i "{audio_file}" \
        # ~-shortest \
        # ~-c:v libvpx \
        # ~-threads 4 \
        # ~-c:a libopus \
        # ~-tile-columns 6 -frame-parallel 1 -auto-alt-ref 1  -lag-in-frames 25 \
        # ~-g 9999 \
        # ~-b:v 0 \
        # ~-b:a 0 \
        # ~-vf "scale={size_x}:trunc(ow/a/2)*2" \
        # ~-pix_fmt yuv420p \
        # ~-f webm \
        # ~-y \
        # ~"{output_file}"
    # ~""".format(
            # ~ffmpeg=FFMPEG_BIN,
            # ~loop_options=loop_options,
            # ~image_file=image_tmp_file_path,
            # ~audio_file=audio_tmp_file_path,
            # ~size_x=size_x,
            # ~output_file=output_tmp_file_path
        # ~)

    args = shlex.split(command)

    # ~print('start ffmpeg')
    # ~proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # out, err = proc.communicate()
    # ~print(out)
    # ~proc = subprocess.Popen(args)
    proc = subprocess.Popen(args, stdout=scripts_log_file, stderr=scripts_log_file)
    # proc = asyncio.create_subprocess_exec(args)
    proc.wait()

    # ~command = 'mv -f "{}" "{}"'.format(output_tmp_file_path, new_output_tmp_file_path)
    # ~args = shlex.split(command)
    # ~proc = subprocess.Popen(args)
    # ~proc.wait()

    command = 'rm "{}"'.format(image_tmp_file_path)
    # ~command = 'rm "{}" &>> {SCRIPTS_LOG_FILE}'.format(image_tmp_file_path, SCRIPTS_LOG_FILE=SCRIPTS_LOG_FILE)
    args = shlex.split(command)
    # ~proc = subprocess.Popen(args)
    proc = subprocess.Popen(args, stdout=scripts_log_file, stderr=scripts_log_file)
    # ~proc.wait()

    command = 'rm "{}"'.format(audio_tmp_file_path)
    # ~command = 'rm "{}" &>> {SCRIPTS_LOG_FILE}'.format(audio_tmp_file_path, SCRIPTS_LOG_FILE=SCRIPTS_LOG_FILE)
    args = shlex.split(command)
    # ~proc = subprocess.Popen(args)
    proc = subprocess.Popen(args, stdout=scripts_log_file, stderr=scripts_log_file)
    # ~proc.wait()

    with open('counter.txt') as f:
        views_couter = int(f.read())
    with open('counter.txt', 'w') as f:
        f.write(str(views_couter+1))

    dump('\t'.join((image_filename, audio_filename, basename, '{:.2f}'.format(os.stat(new_output_tmp_file_path).st_size/1024**2)+'Mb', str(time.time()-begin))))

    scripts_log_file.close()


@route('/mkwebms', method="POST")
def get_params():
    scripts_log_file = open(SCRIPTS_LOG_FILE, 'a')

    try:
        size_x = request.forms.get('image_width', SIZE_X)
    except:
        yield template('<html><body>Error getting size_x</body></html>')
        return


    image_upload = request.files.get('image_file')

    audios_upload = request.files.getall('audio_file')


    total_size_kb = int(float(request.forms.get('total_size_kb', MAX_SIZE_KB)))

    command = '{} {}'.format(FREE_SPACE_SH, total_size_kb)
    args = shlex.split(command)
    proc = subprocess.Popen(args, stdout=scripts_log_file, stderr=scripts_log_file)
    proc.wait()


    image_filename = (image_upload.raw_filename)
    _, image_tmp_file_path = tempfile.mkstemp(suffix=image_filename, dir=TMP_DIR)
    image_upload.save(image_tmp_file_path, overwrite=True)

    if image_filename.lower().endswith('.gif'):
        script_name = ANIM_SH
    else:
        script_name = STATIC_SH


    for audio_upload in audios_upload:
        begin = time.time()

        audio_filename = (audio_upload.raw_filename)

        _, audio_tmp_file_path = tempfile.mkstemp(suffix=audio_filename, dir=TMP_DIR)
        _, output_tmp_file_path = tempfile.mkstemp(suffix=(os.path.splitext(audio_filename)[0]+'.webm'),dir=TMP_DIR)

        basename = os.path.basename(output_tmp_file_path)
        new_output_tmp_file_path = os.path.join(WEBM_CACHE_DIR, basename)

        audio_upload.save(audio_tmp_file_path, overwrite=True)

        # ~yield template('wait.tpl', {'webm_file': '/webms/{}'.format(basename)})
        yield('<p>Converting <a href="{webm_file}">{webm_file}</a>. Please wait...'.format(webm_file='/webms/{}'.format(basename)))

        command = '{script_name} "{image_file}" "{audio_file}" "{output_file}" "{new_output_tmp_file_path}" {size_x}'.format(
            script_name=script_name,
            image_file=image_tmp_file_path,
            audio_file=audio_tmp_file_path,
            output_file=output_tmp_file_path,
            new_output_tmp_file_path=new_output_tmp_file_path,
            size_x=size_x
        )

        args = shlex.split(command)
        proc = subprocess.Popen(args, stdout=scripts_log_file, stderr=scripts_log_file)
        proc.wait()

        yield(' Done</p>')

        command = 'rm "{}"'.format(audio_tmp_file_path)
        args = shlex.split(command)
        proc = subprocess.Popen(args, stdout=scripts_log_file, stderr=scripts_log_file)

        dump('\t'.join((image_filename, audio_filename, basename, '{:.2f}'.format(os.stat(new_output_tmp_file_path).st_size/1024**2)+'Mb', str(time.time()-begin))))

    with open('counter.txt') as f:
        views_couter = int(f.read())
    with open('counter.txt', 'w') as f:
        f.write(str(views_couter+len(audios_upload)))

    command = 'rm "{}"'.format(image_tmp_file_path)
    args = shlex.split(command)
    proc = subprocess.Popen(args, stdout=scripts_log_file, stderr=scripts_log_file)

    scripts_log_file.close()


def dump(msg):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(time.ctime() + ' ' + str(msg) + '\n')

@route('/webms/<filename:path>', name='webms')
def give_webm(filename):
    print('webm given', os.path.join(WEBM_CACHE_DIR, filename))
    return static_file(filename, root=WEBM_CACHE_DIR)

@route('/webmslist')
@view('webmslist')
def show_webms_list():
    webms_list = [os.path.basename(i) for i in sorted(glob.glob(os.path.join(WEBM_CACHE_DIR, '*.*')), key=os.path.getmtime)]
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
