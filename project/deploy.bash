#!/bin/bash
# scp flat files to prod.
# Deploy to QA: ./deploy.bash
# Deploy to prod: ./deploy.bash --server prod
ENVIRON='PROD'
export environ=$ENVIRON
SERVER='qa'
DIR='/apps/'
PROJECT='project-dir-name'
LOCATION_OVERRIDE=0
html_only() { 
    echo ''
}

while [ "$1" != "" ]; do
    case $1 in
        -e | --environ ) shift
            ENVIRON=$1
            ;;
        -p | --project ) shift
            PROJECT=$1
            ;;
        -s | --server ) shift
            SERVER=$1
            ;;
        -d | --dir ) shift
            DIR=$1
            ;;
        -h | --htmlonly ) shift
            html_only() {
                find public \! -name "*.html" -type f -delete;
            }
            ;;
        -f | --freeze ) shift
            python freeze.py; export environ='DEV'; exit 1
            ;;
    esac
    shift
done

# If we bailed on deploy mid-deploy we'll still have the public dir around.
if [ -d "$PROJECT" ]; then rm -fr $PROJECT; fi

#python tests.py && \
html_only && \
    cp -fr csv build && \
    python deploy.py && \
    python freeze.py && \
    mv build $PROJECT && \
    scp -r $PROJECT $SERVER:$DIR && \
    mv $PROJECT build

export environ='DEV'
