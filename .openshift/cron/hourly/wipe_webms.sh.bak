#!/bin/bash
HOURS=48
if [[ $(find $OPENSHIFT_DATA_DIR/last_run -mmin +$(expr ${HOURS} \* 60)) ]]; then #run every 30 mins
  find $OPENSHIFT_DATA_DIR/mkwebm/webms/ -type f -mmin +$(expr ${HOURS} \* 60) -exec rm {} \;
fi
