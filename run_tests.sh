#!/bin/sh

# DOCTESTS ####################################################################

echo
echo
python3 -m doctest ./pywicta/io/images.py
if [ $? -ne 0 ]; then
    exit 1
fi

# UNITTESTS ###################################################################

pytest
