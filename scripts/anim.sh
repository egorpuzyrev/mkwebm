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

TMP_VIDEO=$(mktemp $OPENSHIFT_TMP_DIR/XXXXXXXXX.webm)
${FFMPEG_BIN} -i "${IMAGE}" -c:v libvpx -auto-alt-ref 0 -f webm "${TMP_VIDEO}"

# ~${FFMPEG_BIN}   -hide_banner \
        # ~-loglevel error

# ~${FFMPEG_BIN} -hide_banner \
        # ~-ignore_loop 0 \
        # ~-i "${IMAGE}" \
        # ~-i "${AUDIO}" \
        # ~-shortest \
        # ~-c:v ${VCODEC} \
        # ~-threads 4 \
        # ~-c:a ${ACODEC} \
        # ~-tile-columns 6 -frame-parallel 1 -auto-alt-ref 1  -lag-in-frames 25 \
        # ~-g 9999 \
        # ~-b:v 450k \
        # ~-b:a 0 \
        # ~-pix_fmt yuv420p \
        # ~-f webm \
        # ~-y \
        # ~"${OUTPUT}"


${FFMPEG_BIN} -hide_banner \
        -f lavfi \
        -i "movie=filename=${TMP_VIDEO}:loop=0, setpts=N/(FRAME_RATE*TB)" \
        -i "${AUDIO}" \
        -shortest \
        -c:v ${VCODEC} \
        -threads 4 \
        -c:a ${ACODEC} \
        -tile-columns 6 -frame-parallel 1 -auto-alt-ref 1  -lag-in-frames 25 \
        -g 9999 \
        -b:v 450k \
        -b:a 0 \
        -pix_fmt yuv420p \
        -f webm \
        -y \
        "${OUTPUT}"


mv "${OUTPUT}" "${NEW_OUTPUT}" || true
# ~rm "${IMAGE}" || true
# ~rm "${AUDIO}" || true
