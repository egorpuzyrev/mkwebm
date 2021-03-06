#!/bin/bash
echo "$(date) $0"
# VCODEC="libvpx-vp9"
# ~VCODEC="libvpx"
# ~ACODEC="libopus"
# ~FILE_FORMAT="webm"

# VCODEC="libx264"
# ACODEC="libmp3lame"
# FILE_FORMAT="mpegts"

VCODEC="libxvid"
ACODEC="libmp3lame"
FILE_FORMAT="mp4"
# ~FILE_FORMAT="avi"

# ~FFMPEG_BIN="./ffmpeg/ffmpeg"
FFMPEG_BIN="${OPENSHIFT_REPO_DIR}/ffmpeg/ffmpeg"

IMAGE="${1}"
AUDIO="${2}"
OUTPUT="${3}"
NEW_OUTPUT="${4}"

TMP_VIDEO=$(mktemp $OPENSHIFT_TMP_DIR/XXXXXXXXX.${FILE_FORMAT})
${FFMPEG_BIN} -hide_banner -i "${IMAGE}" -c:v ${VCODEC} -vf "setsar=1/1, scale=trunc(iw/2)*2:trunc(ow/a/2)*2" -pix_fmt yuv420p -f ${FILE_FORMAT} -y "${TMP_VIDEO}"

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


# ~${FFMPEG_BIN} -hide_banner \
        # ~-re \
        # ~-f lavfi \
        # ~-i "movie=filename=${TMP_VIDEO}:loop=0, setpts=N/(FRAME_RATE*TB)" \

${FFMPEG_BIN} -hide_banner \
        -f concat -safe 0 -i <(for i in {1..10000}; do printf "file '%s'\n" ${TMP_VIDEO}; done) \
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
        -vf "setsar=1/1, scale=trunc(iw/2)*2:trunc(ow/a/2)*2" \
        -f ${FILE_FORMAT} \
        -y \
        "${OUTPUT}"


mv "${OUTPUT}" "${NEW_OUTPUT}" || true
# ~rm "${IMAGE}" || true
# ~rm "${AUDIO}" || true
