#!/bin/bash
# Download the existing CSVs from prod

cd csv
for PATH in `ls -R *| awk '
    /:$/&&f{s=$0;f=0}
    /:$/&&!f{sub(/:$/,"");s=$0;f=1;next}
    NF&&f{ print s"/"$0 }' | grep '.csv'`; do /usr/local/bin/wget -O$PATH "http://interactive.nydailynews.com/$PATH"; done

cd ../
