#!/bin/sh

pyinstaller patch.py -F
cp -r patches dist
mkdir -p release
cp -r dist release
mv release/dist release/mcef-codec-patch-linux64
cd release
zip -r mcef-codec-patch-linux64.zip mcef-codec-patch-linux64

echo "Done"
