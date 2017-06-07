#!/bin/bash

# VCODEC="libvpx-vp9"
VCODEC="libvpx"
ACODEC="libopus"

# ~FFMPEG_BIN="./ffmpeg/ffmpeg-3.2-64bit-static/ffmpeg"
FFMPEG_BIN="${OPENSHIFT_REPO_DIR}/ffmpeg/ffmpeg"

IMAGE="${1}"
AUDIO="${2}"
OUTPUT="${3}"
NEW_OUTPUT="${4}"

WIDTH="${5}"


# ~${FFMPEG_BIN}   -hide_banner \
        # ~-loglevel error

${FFMPEG_BIN} -hide_banner \
        -loop 1 \
        -r 1 \
        -i "${IMAGE}" \
        -i "${AUDIO}" \
        -shortest \
        -c:v ${VCODEC} \
        -threads 4 \
        -c:a ${ACODEC} \
        -tile-columns 6 -frame-parallel 1 -auto-alt-ref 1  -lag-in-frames 25 \
        -g 9999 \
        -b:v 450k \
        -b:a 0 \
        -vf "scale=${WIDTH}:trunc(ow/a/2)*2" \
        -pix_fmt yuv420p \
        -f webm \
        -y \
        "${OUTPUT}"

mv "${OUTPUT}" "${NEW_OUTPUT}" || true
rm "${IMAGE}" || true
rm "${AUDIO}" || true
