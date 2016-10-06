#!/bin/bash
if [ ! -f $OPENSHIFT_DATA_DIR/last_run ]; then
  touch $OPENSHIFT_DATA_DIR/last_run
fi
if [[ $(find $OPENSHIFT_DATA_DIR/last_run -mmin +29) ]]; then #run every 30 mins
  touch $OPENSHIFT_DATA_DIR/last_run
  find $OPENSHIFT_DATA_DIR/mkwebm/webms/ -type f -mmin +29 -exec rm {} \;
fi
