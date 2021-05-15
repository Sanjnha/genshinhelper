#! /bin/bash

TEMP_PATH="temp"
DIST_PATH="dist"

mkdir ${TEMP_PATH}

if [ ! -d "${DIST_PATH}" ]; then
  mkdir ${DIST_PATH}
fi

pip install genshinhelper -t ${TEMP_PATH}

cd ${TEMP_PATH}

cat>index.py<<EOF
from genshinhelper import main 

def main_handler(event, context):
    main()
EOF

VERSION=`cat genshinhelper/_version.py | sed 's/[^0-9.]*\([0-9.]*\).*/\1/'`
FILE_DATE=`date +%Y%m%d`
FILE_NAME="genshinhelper-${VERSION}-${FILE_DATE}-serverless.zip"

zip -r ${FILE_NAME} *  

cd .. && mv ${TEMP_PATH}/${FILE_NAME} ${DIST_PATH} && rm -rf ${TEMP_PATH}
