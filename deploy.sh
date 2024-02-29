#!/bin/bash
#
#
#
mkdir dist
rm -r dist/*
python setup.py sdist bdist_wheel

echo "Enter Your Twine Key: "
read twine_key
twine upload -u __token__ -p $twine_key dist/*
