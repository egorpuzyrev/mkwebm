#!/bin/bash


    # ~Your gear’s data directory

    # ~/tmp

    # ~Your Git repository on the gear

    # ~The log files for your application and database servers

    # ~The data files for your database server

SIZE_LIMIT_KB=$(expr 1000 \* 1024 - 180000)
SIZE_NEEDED_KB=$(expr ${1} \* 3)
NFILES_TO_DELETE=2

WEBMS_DIR="${OPENSHIFT_DATA_DIR}/mkwebm/webms"
# ~LOG_FILE=""

# ~DIRECTORIES=" ${OPENSHIFT_DATA_DIR} ${OPENSHIFT_TMP_DIR} ${OPENSHIFT_REPO_DIR} ${OPENSHIFT_LOG_DIR}"
DIRECTORIES="${OPENSHIFT_HOMEDIR} ${OPENSHIFT_TMP_DIR}"

TOTAL_SIZE_KB=$(du -kcs ${DIRECTORIES} 2>/dev/null | tail -n1 | cut -f 1)
SPACE_LEFT_KB=$(expr ${SIZE_LIMIT_KB} - ${TOTAL_SIZE_KB})

while [[ ${SPACE_LEFT_KB} -lt ${SIZE_NEEDED_KB} ]] && [ "$(ls -A ${WEBMS_DIR})" ]; do

    # ~pushd  ${WEBMS_DIR} && ls -tp | grep -v '/$' | tail -n ${NFILES_TO_DELETE} | xargs -d '\n' rm -- && popd
    pushd ${WEBMS_DIR}
    ls -tp | grep -v '/$' | tail -n ${NFILES_TO_DELETE} | xargs -d '\n' rm --
    popd

    TOTAL_SIZE_KB=$(du -kcs ${DIRECTORIES} 2>/dev/null | tail -n1 | cut -f 1)
    SPACE_LEFT_KB=$(expr ${SIZE_LIMIT_KB} - ${TOTAL_SIZE_KB})

done;
