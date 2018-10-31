#!/bin/bash

BRANCH=${1:-master}
mkdir -p debian/var/www/env/amoveo-explorer/app >/dev/null 2>&1
rm -rf debian/var/www/env/amoveo-explorer/*

VERSION=$(git describe --always --tags | sed -re "s/-/~${BRANCH}+/" | sed -re 's/^[^0-9]//g')

rm -rf build
mkdir build

virtualenv -p python3.5 build/env
build/env/bin/pip install ..

fpm -s dir -t deb \
    -n exantech-amoveo-explorer \
    -v ${VERSION} \
    -a all \
    -d python3.5 \
    -d libpython3.5 \
    -d libpq5 \
    --prefix=/ \
    --post-install=debian/postinst \
    ../service/=/var/www/env/amoveo-explorer/service/ \
    ./build/env/lib/=/var/www/env/amoveo-explorer/lib/ \
    ./build/env/bin/=/var/www/env/amoveo-explorer/bin/ \
    ./debian/etc/=/etc/ \
